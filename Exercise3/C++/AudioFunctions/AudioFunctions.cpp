#include "AudioFunctions.h"

using namespace std;

const int MINIMUM_VOLUME (-4000);

AudioFunctions::AudioFunctions() {

	mp_filter_graph_manager = NULL;
	mp_media_control = NULL;
	mp_media_seeking = NULL;
	mp_basic_audio = NULL;

	mp_current_state = State_Stopped;

	m_file_name.Empty();
	m_file_path.Empty();

	m_released = TRUE;
}

AudioFunctions::~AudioFunctions() {
	// If the clients didn't FreeDirectShow by themselves, we help them release it
	if (m_released != TRUE) {
		FreeDirectShow();
	}
}

void AudioFunctions::InitDirectShow() {
	HRESULT h_result = CoInitialize(NULL);
	if (FAILED(h_result)) {
		printf("ERROR - Could not initialize COM library");
		return;
	}

	InitMedia("");
	if (FAILED(h_result)) {
		printf("Can't initialize the playback");
	}
	m_released = FALSE;
}

void AudioFunctions::FreeDirectShow() {

	// Clean up.	
	mp_media_control->Release();
	mp_media_control = NULL;

	mp_media_seeking->Release();
	mp_media_seeking = NULL;

	mp_basic_audio->Release();
	mp_basic_audio = NULL;

	mp_filter_graph_manager->Release();
	mp_filter_graph_manager = NULL;

	CoUninitialize();

	m_released = TRUE;
}

void AudioFunctions::OpenMedia(wchar_t *path) {
	StopMedia();
	CString file_path(path);
	HRESULT h_result = InitMedia(file_path);

	if (FAILED(h_result)) {
		printf("Can't initialize the playback");
	}
}

void AudioFunctions::PlayMedia() { 
	mp_media_control->Run();
	mp_current_state = State_Running;
} 

void AudioFunctions::PauseMedia() {  
	mp_media_control->Pause();
	mp_current_state = State_Paused;
}

void AudioFunctions::StopMedia() {  
	mp_media_control->Stop();
	mp_current_state = State_Stopped;

	// Reset to beginning of media clip
	LONGLONG position = 0;
	mp_media_seeking->SetPositions(&position, AM_SEEKING_AbsolutePositioning, NULL, AM_SEEKING_NoPositioning);
}

int AudioFunctions::GetCurrentState() {
	if (mp_current_state == State_Stopped) {
		return 0;
	}
	else if (mp_current_state == State_Paused) {
		return 1;
	}
	else if (mp_current_state == State_Running) {
		return 2;
	}

	// Shouldn't reach this statement
	return -1;
}

int AudioFunctions::GetMediaPosition() {
	REFERENCE_TIME current_reference_time;
	mp_media_seeking->GetCurrentPosition(&current_reference_time);

	// Convert the LONGLONG duration into human-readable format
	unsigned long total_ms = (unsigned long) ((float) current_reference_time / 10000.0); // 100ns -> ms
	int total_s = total_ms / (int) 1000;

	return total_s;
}

int AudioFunctions::GetMediaDuration() {
	REFERENCE_TIME duration;
	mp_media_seeking->GetDuration(&duration);

	// Convert the LONGLONG duration into human-readable format
	unsigned long total_ms = (unsigned long) ((float)duration / 10000.0); // 100ns -> ms
	int total_s = total_ms / (int) 1000;

	return total_s;
}

PyObject *AudioFunctions::GetFilePath() {  

	if (!m_file_name.IsEmpty()) {
		PyObject *return_string = Py_BuildValue("u", m_file_path);
		return return_string;
	}
	else {
		return Py_BuildValue("");
	}
}

void AudioFunctions::SetVolume(double offset) {
	// Set new volume
	mp_basic_audio->put_Volume(MINIMUM_VOLUME + (1.0 - offset) * -MINIMUM_VOLUME);
}

void AudioFunctions::SetMediaPosition(double offset) {
	REFERENCE_TIME duration;
	mp_media_seeking->GetDuration(&duration);

	// Update the position continuously.
	REFERENCE_TIME new_reference_time = (duration * offset);

	mp_media_seeking->SetPositions(&new_reference_time, AM_SEEKING_AbsolutePositioning, NULL, AM_SEEKING_NoPositioning);
}

PyObject *AudioFunctions::OpenFileDialog() {  
	CString file_filter = ".mp3|*.mp3||";
	CFileDialog fd(TRUE, L"mp3", L"*.mp3", OFN_HIDEREADONLY, file_filter);

	if (fd.DoModal() == IDOK) {
		m_file_path = fd.GetPathName();
		m_file_name = fd.GetFileName();
		
		StopMedia();

		HRESULT h_result = InitMedia(m_file_path);	
		if (FAILED(h_result)) {
			return Py_BuildValue("");
		}
		else {
			return Py_BuildValue("u", m_file_name);
		}

	}
	else {
		return Py_BuildValue("");
	}
}

HRESULT AudioFunctions::InitMedia(CString file_path) { 
	HRESULT h_result;
	
	h_result = CoCreateInstance(CLSID_FilterGraph, NULL, CLSCTX_INPROC, IID_IGraphBuilder, (void **)&mp_filter_graph_manager);
	if (FAILED(h_result)) {
		printf("Can't create FilterGraph instance");
		return E_FAIL;
	}

	h_result = mp_filter_graph_manager->QueryInterface(IID_IMediaControl, (void **)&mp_media_control);
	if (FAILED(h_result)) {
		printf("Can't query MediaControl interface");
		return E_FAIL;
	}

	h_result = mp_filter_graph_manager->QueryInterface(IID_IMediaSeeking, (void **)&mp_media_seeking);
	if (FAILED(h_result)) {
		printf("Can't query MediaSeeking interface");
		return E_FAIL;
	}

	h_result = mp_filter_graph_manager->QueryInterface(IID_IBasicAudio, (void **)&mp_basic_audio);
	if (FAILED(h_result)) {
		printf("Can't query BasicAudio interface");
		return E_FAIL;
	}

	if (file_path != "") {
		mp_filter_graph_manager->RenderFile(file_path.AllocSysString(), NULL);
		if (FAILED(h_result)) {
			printf("Can't render the file");
			return E_FAIL;
		}
	}
	return S_OK;
}


