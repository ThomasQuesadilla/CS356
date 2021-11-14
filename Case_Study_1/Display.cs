using System.Collections;
using System.IO;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

public class Display : MonoBehaviour
{
    string[] list_location;
    string pose_string;
    int idx=0;
    byte[] framebyte;
    int pose_length;
    Texture2D VRtexture;
    int resWidth = 960;
    int resHeight = 540;
    RawImage rawImage;
    // Start is called before the first frame update
    void Start()
    {
        Application.targetFrameRate = 30;
        //Fill in start
        //Please change the directory of "pose.txt".
        list_location = ReadStream("pose.txt");
        //Fill in end
        pose_length = list_location.Length;
        VRtexture = new Texture2D(resWidth, resHeight, TextureFormat.RGB24, false);
        rawImage = GetComponent<RawImage>();
    }

    // Update is called once per frame
    void Update()
    {
        StartCoroutine(UploadPose());
        StartCoroutine(ReadFrame());
    }

    IEnumerator UploadPose()
    {
        pose_string = list_location[idx];
        if (idx <= pose_length - 1)
        {
            idx = idx + 1;
        }
        else
        {
            idx = idx + 1 - pose_length;
        }
        //Fill in start
        // Please change http://10.197.249.134:5000/pose to your server IP address and port
        using (UnityWebRequest www = UnityWebRequest.Put("http://10.197.249.134:5000/pose", pose_string))
        //Fill in end
        {
            yield return www.SendWebRequest();
            if (www.responseCode != 200)
            {
                Debug.Log(www.error);
            }
        }
    }

    IEnumerator ReadFrame()
    {
        //Fill in start
        // Please change http://10.197.249.134:5000/frame to your server IP address and port
        using (UnityWebRequest webRequest = UnityWebRequest.Get("http://10.197.249.134:5000/frame"))
        //Fill in end
        {
            yield return webRequest.SendWebRequest();
            if (webRequest.responseCode == 200)
            {
                framebyte = webRequest.downloadHandler.data;
                Debug.Log(framebyte.Length);
                VRtexture.LoadImage(framebyte);
                rawImage.texture = VRtexture;
            }
            else
            {
                Debug.Log(webRequest.error);
            }
        }
    }


    public string[] ReadStream(string path)
    {
        string[] list = File.ReadAllLines(path);
        return list;
    }
}
