using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LoginManager : MonoBehaviour
{
    public InputField ui_username;
    public InputField ui_password;
    public Button ui_login;
    public GameObject obj_game_play;

    /// <summary>
    /// 按下登陆按钮
    /// </summary>
    public void LoginClick()
    {
        Debug.Log("login click");
        string username = ui_username.text;
        string password = ui_password.text;
        if(username==null || password == null)
        {
            return;
        }

        Request login = new Request();
        login.type = 0;
        SendData tem = new SendData();
        tem.username = username;
        tem.password = password;
        tem.room_id = 0;
        login.data = tem;

        NetComponent.Instance.SendMessage(login);

    }

    /// <summary>
    /// 登陆返回信息处理
    /// </summary>
    public void LoginRespone()
    {
        gameObject.SetActive(false);
        ui_username.text = "";
        ui_password.text = "";
        obj_game_play.SetActive(true);
        obj_game_play.GetComponent<GamePlayManager>().SendRiotData();
    }

}
