#ifndef AUDIOFUNCTIONS_H_
#define AUDIOFUNCTIONS_H_

#include <tchar.h>
#include <afxdlgs.h>
#include <atlstr.h>

#include <dshow.h>

#include <python.h>

class AudioFunctions { 
public: 
	// Functions provided for AudioBox
    AudioFunctions();
	~AudioFunctions();

	void InitDirectShow();
	void FreeDirectShow();

	void OpenMedia(wchar_t *path);
	void PlayMedia();
	void PauseMedia();
	void StopMedia();
	
	int GetCurrentState();
	int GetMediaPosition();
	int GetMediaDuration();
	PyObject *GetFilePath();

	void SetVolume(double volume);
	void SetMediaPosition(double offset);

	PyObject *OpenFileDialog();
	////////////////////////////////

	

	CString m_file_name;
	CString m_file_path;

private:
	IGraphBuilder *mp_filter_graph_manager;
	IMediaControl *mp_media_control;
	IMediaSeeking *mp_media_seeking;
	IBasicAudio   *mp_basic_audio;

	FILTER_STATE mp_current_state;

	bool m_released;

	HRESULT InitMedia(CString file_path);
};

#endif