using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Net;
using System;
using UnityEngine;
using Newtonsoft.Json;
using System.Text;


public class MessagePacket
{
    public Session session;
    public Response response;
    public MessagePacket(Session _s,Response _r)
    {
        session = _s;
        response = _r;
    }
}

class PEPkg
{
    public int headLen = 4;
    public byte[] headBuff = null;
    public int headIndex = 0;

    public int bodyLen = 0;
    public byte[] bodyBuff = null;
    public int bodyIndex = 0;

    public PEPkg()
    {
        headBuff = new byte[4];
    }

    public void InitBodyBuff()
    {
        Array.Reverse(headBuff);  //IPAddress.NetworkToHostOrder(messageLen)
        bodyLen = BitConverter.ToInt32(headBuff, 0);
        //int real_len = IPAddress.NetworkToHostOrder(bodyLen);
        bodyBuff = new byte[bodyLen];
    }

    public void ResetData()
    {
        headIndex = 0;
        bodyLen = 0;
        bodyBuff = null;
        bodyIndex = 0;
    }
}
public class Session
{
    private Socket socket = null;
    private Action closeCB;

    /// <summary>
    /// 链接
    /// </summary>
    protected void onConnect()
    {
        Debug.Log("成功链接服务器");
    }

    /// <summary>
    /// 离线
    /// </summary>
    protected void onDisconnected()
    {

    }

    /// <summary>
    /// 收到server的消息
    /// </summary>
    /// <param name="msg"></param>
    protected void onRecive(byte[] msg)
    {
        var string_msg = Encoding.UTF8.GetString(msg);
        var msg_data = JsonConvert.DeserializeObject<Response>(string_msg);
        var msg_packet = new MessagePacket(this, msg_data);
        Debug.Log($"当前收到消息，内容为{string_msg}");
        NetComponent.Instance.m_sessin_queque.Enqueue(msg_packet);
    }

    /// <summary>
    /// 开始接收消息
    /// </summary>
    /// <param name="skt">客户端的socket</param>
    /// <param name="call_back">回调函数</param>
    public void StartReciveData(Socket skt , Action call_back)
    {
        try
        {
            this.socket = skt;
            this.closeCB = call_back;
            onConnect();
            PEPkg pe_pkt = new PEPkg();
            socket.BeginReceive(pe_pkt.headBuff, 0, pe_pkt.headLen, SocketFlags.None, new AsyncCallback(ReciveHead), pe_pkt);

        }
        catch(Exception e)
        {
            Debug.LogWarning(e);
        }
    }

    private void ReciveHead(IAsyncResult ar)
    {
        try
        {
            PEPkg pack = (PEPkg)ar.AsyncState;
            if (socket.Available == 0)
            {
                onDisconnected();
                Clear();
                return;
            }
            int len = socket.EndReceive(ar);
            if (len > 0)
            {
                pack.headIndex += len;
                if (pack.headIndex < pack.headLen)
                {
                    socket.BeginReceive(
                        pack.headBuff,
                        pack.headIndex,
                        pack.headLen - pack.headIndex,
                        SocketFlags.None,
                        new AsyncCallback(ReciveHead),
                        pack);
                }
                else
                {
                    pack.InitBodyBuff();
                    socket.BeginReceive(pack.bodyBuff,
                        0,
                        pack.bodyLen,
                        SocketFlags.None,
                        new AsyncCallback(RcvBodyData),
                        pack);
                }
            }
            else
            {
                onDisconnected();
                Clear();
            }
        }
        catch (Exception e)
        {
            Debug.LogWarning(e);
        }
    }


    private void RcvBodyData(IAsyncResult ar)
    {
        try
        {
            PEPkg pack = (PEPkg)ar.AsyncState;
            int len = socket.EndReceive(ar);
            if (len > 0)
            {
                pack.bodyIndex += len;
                if (pack.bodyIndex < pack.bodyLen)
                {
                    socket.BeginReceive(pack.bodyBuff,
                        pack.bodyIndex,
                        pack.bodyLen - pack.bodyIndex,
                        SocketFlags.None,
                        new AsyncCallback(RcvBodyData),
                        pack);
                }
                else
                {
                    onRecive(pack.bodyBuff);

                    //loop recive
                    pack.ResetData();
                    socket.BeginReceive(
                        pack.headBuff,
                        0,
                        pack.headLen,
                        SocketFlags.None,
                        new AsyncCallback(ReciveHead),
                        pack);
                }
            }
            else
            {
                onDisconnected();
                Clear();
            }
        }
        catch (Exception e)
        {
            Debug.LogWarning(e);
        }
    }

    private void Clear()
    {
        if (closeCB != null)
        {
            closeCB();
        }
        Debug.Log("??????????????");
        socket.Close();
    }


    
}

public class Network
{
    public static Socket socket = null;
    public Network()
    {
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
    }

    public void StartClient(string ip,int port)
    {
        try
        {
            socket.BeginConnect(new IPEndPoint(IPAddress.Parse(ip), port), new AsyncCallback(ClientConnected), socket);
        }
        catch(Exception e)
        {
            Debug.Log(e);
        }
    }

    void ClientConnected(IAsyncResult ar)
    {
        try
        {
            socket.EndConnect(ar);
            Session sess = new Session();
            sess.StartReciveData(socket,null);

        }
        catch(Exception e)
        {
            Debug.Log(e);
        }
    }

    public void Close()
    {
        if (socket!=null)
        {
            socket.Close();
        }
    }
}
