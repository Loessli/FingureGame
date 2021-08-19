using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

/// <summary>
/// 上行包
/// </summary>
public class Request
{
    public int type;
    public SendData data;
}

/// <summary>
/// 下行包
/// </summary>
public class Response
{
    public int type;
    public ReciveData data;
}

public class SendData
{
    public string username;
    public string password;
    public int room_id;  //房间ID
    public int play_state; //游戏中的状态
    public int play_order; //剪刀0,石头1,布2命令
    public bool leave_room;
}

public class ReciveData
{
    public int room_id;
    public bool game_ready; //是否两个人
    public bool is_over; //游戏是否结束
    public int play_result; //1胜利，2失败，3平局
    public bool login_result; //登陆结果
    public string error_msg;
}


