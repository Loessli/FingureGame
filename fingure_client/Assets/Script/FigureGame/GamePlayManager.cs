using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


public class GamePlayManager : MonoBehaviour
{

    public Text ui_message_show;
    public Button ui_scissons;
    public Button ui_stone;
    public Button ui_paper;
    public GameObject login_ui;
    public GameObject game_play_ui;

    //
    private int m_play_order;
    private Request req_data;
    private int m_room_id;
    private int m_play_state;


    void Awake()
    {
        ui_message_show.text = "Waiting for gameing!";
        req_data = new Request()
        {
            type = 1
        };
    }


    public void GamePlayResponse(ReciveData recive)
    {
        m_room_id = recive.room_id;

        //如果还没有结果
        if (!recive.is_over)
        {
            if (recive.game_ready) //游戏开始
            {
                ActiveButton();
                SetTextMsg("Please riot!");
            }
            else //还差一个人，等待
            {
                SetTextMsg("Please wait for another player!");
            }
        }
        //如果已经有了结果
        else
        {
            string temp_result = "";
            switch (recive.play_result)
            {
                case 1:
                    temp_result = "Win!";
                    break;
                case 2:
                    temp_result = "Lose!";
                    break;
                case 3:
                    temp_result = "Draw!(平局)";
                    break;
                default:
                    Debug.Log("?????????????结果返回有问题");
                    break;
            }
            ActiveButton();
            SetTextMsg(temp_result + "Please riot!");
        }
        
    }

    public void SendRiotData()
    {
        SendData send_data = new SendData();
        send_data.room_id = m_room_id;
        send_data.play_state = m_play_state;
        send_data.play_order = m_play_order;
        req_data.data = send_data;
        NetComponent.Instance.SendMessage(req_data);
        ResetSendData();
    }

    public void LeaveRoom()
    {
        SendData send_data = new SendData();
        send_data.room_id = m_room_id;
        send_data.leave_room = true;
        req_data.data = send_data;
        NetComponent.Instance.SendMessage(req_data);
        m_play_order = 0;
        m_room_id = 0;
        login_ui.SetActive(true);
        game_play_ui.SetActive(false);

    }

    private void PlayGame()
    {
        DeActiveButton();
        SendRiotData();
    }

    private void SetTextMsg(string msg)
    {
        ui_message_show.text = msg;
    }

    private void ResetSendData()
    {
        m_play_order = -1;
        m_play_state = 0;
    }
    private void DeActiveButton()
    {
        ui_scissons.interactable = false;
        ui_stone.interactable = false;
        ui_paper.interactable = false;
    }

    private void ActiveButton()
    {
        ui_scissons.interactable = true;
        ui_stone.interactable = true;
        ui_paper.interactable = true;
    }

    public void ScissonsClick()
    {
        m_play_order = 0;
        m_play_state = 1;
        DeActiveButton();
        SendRiotData();
    }

    public void StoneClick()
    {
        m_play_order = 1;
        m_play_state = 1;
        DeActiveButton();
        SendRiotData();
    }

    public void PaperClick()
    {
        m_play_order = 2;
        m_play_state = 1;
        DeActiveButton();
        SendRiotData();
    }
}
