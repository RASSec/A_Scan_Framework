/**
 * Created by Administrator on 2018/3/14.
 */


/*
*帖子点赞
 */

function thumb(ar_id){
        var userid = getCookie("userid");
        alert(userid)
        $.ajax({
            url:"/api/thumb",
            method:"POST",
            data:{"arid":ar_id,"userid":userid},
            success:function (res) {
                // alert(res.info);
                if (res.code == 0){
                    alert("点赞成功");
                    //alert($(this).$(".thumb_num").text())//点赞数+1,前端手动加，不请求服务器，减少服务器的压力
                }else if (res.code == 1){
                    alert("已点赞，请勿重复点赞");
                }else {
                    alert("点赞失败")
                }

            },
            error:function () {
                console.log("erro");
            }

        })
        }

/**
 *
 * 登录用户是否已点赞
 */















