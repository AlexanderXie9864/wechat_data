  $.ajax(
                {
                    url:'/da/infoCheck',
                    type:'POST',
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify(data),
                    dataType:"json",
                    success:function (data) {
                        if(data.msg==='exist')
                        {
                            alert('该用户数据已经采集完毕，请勿重复采集！');
                             window.location.reload();

                        }
                        else if(data.msg==='success')
                        {
                            $("#form").submit();
                            var index=layer.msg('加载中', {
                                          icon: 16
                                          ,shade: 0.01
                                        });
                            var t =setTimeout(
                                "   layer.open({\n" +
                                "                                type: 1,\n" +
                                "                                shade: false,\n" +
                                "                                title: false, //不显示标题\n" +
                                "                                content: $('.modal'), //捕获的元素，注意：最好该指定的元素要存放在body最外层，否则可能被其它的相对元素所影响\n" +
                                "                                success:function(){\n" +
                                "                                     $('.modal').show();\n" +
                                "                                     $('.qrcode').show();\n" +
                                "                                       var ref = setInterval(function(){  //6秒自动刷新一次二维码\n" +
                                "                                        $('.qrcode').click();\n" +
                                "                                    },6000);"+
                                "                                },\n" +
                                "                                cancel:function () {\n" +
                                 "                                   if(confirm('点击关闭将取消采集，是否取消？')){\n" +
                                    "                                    $('.modal').hide();\n" +
                                "                                    $('.qrcode').hide();\n" +
                                "                                    window.location.reload();\n" +
                                   "                                     }else{\n"+
                                                           "                     alert('采集进行中，请不要刷新页面或点击关闭按钮...');return false;}\n"+

                                "                                },\n" +
                                "\n" +
                                "                            });"
                                ,
                                2000);

                        }
                        else if(data.msg==='instance_error') {
                            alert('无法创建实例，请重试！');
                            window.location.replace('/');
                        }

                    },
                    error:function (data) {
                        alert('请求失败，出现异常！！！');
                        return false;
                    }

                }
            )