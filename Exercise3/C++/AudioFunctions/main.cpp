#include "AudioFunctions.h"

int main () {
	AudioFunctions test;

	test.InitDirectShow();


	//test.mp_filter_graph_manager->RenderFile(L"C:\\Users\\MarkKC_Ma\\Desktop\\Love Distance Long Affair.mp3", NULL);

    // Run the graph.
	//test.mp_media_control->Run();

    // Block until the user clicks the OK button. 
    // The filter graph runs on a separate thread.
    //MessageBox(NULL, "Click me to end playback.", "DirectShow", MB_OK);

	test.FreeDirectShow();
	
	return 0;
}