/**
 * Created by Administrator on 2018/3/20.
 */




$(document).ready(function () {

    //注册

    $("#regist").click(function () {
        // alert("我要注册了");

    })




    //登录

    $("#login").click(function () {
        var username = $("#username").val();
        var password = $("#password").val();
        console.log(username,password);
        $.ajax({
            url:"/api/login_check",
            method:"POST",
            data:{"password":password,"username":username},
            success:function (res) {
                console.log(res);
                if(res.code==2001){
                    //保存cookie
                    // alert(res.userid);
                    setCookie('userid', res.userid, { expires: 7 });
                    window.location.href="/";
                }else if (res.code==4001){
                    $(".errors").text("用户名或者密码错误，请重试").css({"color":"red"});
                }else{

                }
            }

        })
    });
//退出登录
    $("#logout").click(function () {
        // alert("ok")
        $.ajax({
            url:"/api/logout",
            method:"POST",
            data:{"id":1},
            success:function (res) {
                console.log(res);
                if(res.code==2001){
                    window.location.href="/";
                }
            }

        })
    })

});