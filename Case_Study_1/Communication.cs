using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.Networking;

public class Communication : MonoBehaviour
{
    Camera snapCam;
    byte[] VRframe;
    string pose_string;
    string[] pose;
    Texture2D VRtexture;
    //resolution of the VR frame.
    int resWidth = 960;
    int resHeight = 540;

    private void Start()
    {
        snapCam = GetComponent<Camera>();
        if (snapCam.targetTexture == null)
        {
            snapCam.targetTexture = new UnityEngine.RenderTexture(resWidth, resHeight, 24);
        }
        else
        {
            resWidth = snapCam.targetTexture.width;
            resHeight = snapCam.targetTexture.height;
        }
        VRtexture = new Texture2D(resWidth, resHeight, TextureFormat.RGB24, false);
    }
    void Update()
    {
        StartCoroutine(ReadPose());
        StartCoroutine(UploadFrame());
    }

    IEnumerator ReadPose()
    {
        //Fill in start
        //Please change http://10.197.249.134:5000/pose to your server IP address and port
        using (UnityWebRequest webRequest = UnityWebRequest.Get("http://10.197.249.134:5000/pose"))
        //Fill in end
        {
            yield return webRequest.SendWebRequest();
            if (webRequest.responseCode == 200)
            {
                pose_string = webRequest.downloadHandler.text;
            }
            else
            {
                Debug.Log(webRequest.error);
            }
        }
    }

    IEnumerator UploadFrame()
    {
       
        pose = pose_string.Split(',');
        //set the position and eulerAngles of the camera to the one read from the http server.
        transform.position = new Vector3(float.Parse(pose[1]), float.Parse(pose[2]), float.Parse(pose[3]));
        transform.eulerAngles = new Vector3(float.Parse(pose[4]), float.Parse(pose[5]), float.Parse(pose[6]));
        snapCam.Render();
        UnityEngine.RenderTexture.active = snapCam.targetTexture;
        VRtexture.ReadPixels(new Rect(0, 0, resWidth, resHeight), 0, 0);
        VRframe = VRtexture.EncodeToPNG();
        //Fill in start
        //Please change http://10.197.249.134:5000/frame to your server IP address and port
        using (UnityWebRequest www = UnityWebRequest.Put("http://10.197.249.134:5000/frame", VRframe))
        //Fill in end
        {
            yield return www.SendWebRequest();
            if (www.responseCode != 200)
            {
                Debug.Log(www.error);
            }
        }
    }
}
