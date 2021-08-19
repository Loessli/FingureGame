using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;
using System.Text;
using System.Net.Sockets;
using System.IO;
using System.Net;

public class NetComponent : MonoBehaviour
{
    //script component variables
    public LoginManager login_manager;
    public GamePlayManager game_play_manager;

    //net variables
    public Queue<MessagePacket> m_sessin_queque = null;
    public static NetComponent Instance = null;
    /// <summary>
    /// 初始化
    /// </summary>
    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
        m_sessin_queque = new Queue<MessagePacket>();
        new Network().StartClient("10.1.55.77", 12456);


        login_manager.gameObject.SetActive(true);
    }


    /// <summary>
    /// 服务器回包消息处理
    /// </summary>
    /// <param name="msg_pkt">回包内容</param>
    void HandleMassage(MessagePacket msg_pkt)
    {
        int func_type = msg_pkt.response.type;
        ReciveData rsp_data = msg_pkt.response.data;
        if (func_type == 0)
        {
            if (rsp_data.login_result)
            {
                login_manager.LoginRespone();
            }
        }
        else if(func_type == 1)
        {
            game_play_manager.GamePlayResponse(rsp_data);
        }
    }

    /// <summary>
    /// tick
    /// </summary>
    void Update()
    {
        lock ("gameObject")
        {
            if (m_sessin_queque.Count>0)
            {
                var msg_pkt = m_sessin_queque.Dequeue();
                HandleMassage(msg_pkt);
            }
        }
    }

    /// <summary>
    /// 给服务器发送消息
    /// </summary>
    /// <param name="req">发送的内容</param>
    public void SendMessage(Request req)
    {
        string data = JsonConvert.SerializeObject(req);
        byte[] buffer = Encoding.UTF8.GetBytes(data);

        MemoryStream ms = null;
        using (ms = new MemoryStream())
        {
            ms.Position = 0;
            BinaryWriter writer = new BinaryWriter(ms);
            int size = IPAddress.HostToNetworkOrder(buffer.Length);
            writer.Write(size);
            writer.Write(buffer);
            writer.Flush();
            byte[] send_buffer = ms.ToArray();
            Network.socket.Send(send_buffer);
        }
    }

    private void OnApplicationQuit()
    {
        if (Network.socket != null)
        {
            Network.socket.Close();
        }
        else
        {
            Debug.Log("Quit game");
        }
    }
}
