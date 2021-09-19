Unfortunately, Toon Boom Harmony does not currently support native python scripting. It does provide what's called a "wrapper" that allows JavaScript to run python code, but still requires knowing some JavaScript to use. **There is also no python API**, meaning it's not possible to modify a Harmony scene from python. The main benefit appears to be that you can still create UI from python - meaning you could make dialogs and use them to process data external to Harmony, like processing image files, talking to shotgun/ftrack, etc...

# JavaScript Editor
You can open the JavaScript editor using `Windows > Script Editor`

Details about the script editor UI can be found [here](https://docs.toonboom.com/help/harmony-20/essentials/reference/view/script-editor-view.html?Highlight=script%20editor).

More information on using the script editor can be found [here](https://docs.toonboom.com/help/harmony-20/essentials/scripting/create-qt-script.html). Open the dropdown for "How to create a script" for a step by step guide, and use the index on the right to navigate to related topics.

# Python from JavaScript
To run python code from javascript you must use the [python wrapper](https://docs.toonboom.com/help/harmony-20/scripting/extended/module-PythonManager-PyObjectWrapper.html). You can pass it any python file, and it will run the code. You can also pass values between JavaScript and Python using the methods discussed in the wrapper's documentation.

# Advanced Setup
For those really wanting to use python with Harmony, it's possible to run python in a separate process and communicate via a network socket by creating a javascript server and python client. If you don't know what that means, prepare for a lot of research, or to not use python in Harmony :)

The [shotgun toolkit integration for Harmony](https://github.com/diegogarciahuerta/tk-harmony) is an excellent example of how this can be done. The core operations for interacting with the Harmony software (importing files, saving scene, etc...) are defined in the `configure.js` file. The bootstrap function then [starts the python process](https://github.com/diegogarciahuerta/tk-harmony/blob/master/resources/packages/ShotgunBridge/configure.js#L1543) and communicates with it using the [Server object](https://github.com/diegogarciahuerta/tk-harmony/blob/master/resources/packages/ShotgunBridge/configure.js#L755). The python process is running the [python application](https://github.com/diegogarciahuerta/tk-harmony/blob/master/python/tk_harmony/application.py) which uses the [python client](https://github.com/diegogarciahuerta/tk-harmony/blob/master/python/tk_harmony/client.py) to send requests for those core operations to the javascript server and interprets the responses. This way, the python code is doing the main body of processing, but still able to interact with Harmony.
