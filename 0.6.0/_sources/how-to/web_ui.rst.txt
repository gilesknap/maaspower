Power Config via Web UI
-----------------------

For those power control devices that are configured by a web UI only we provide
a Web Scraping device type.

This has been tested with the Netgear GS3008EP. We have tried to make a generic
DLS that allows for most possible sequences of Web Element interactions but 
YMMV. 

To experiment with the approach and develop your own command sequences for
this device type [see this playground script](../../../utils/webtest.py)



















API Notes for GS308EP
=====================

In the case of the Netgear GS308EP there is an underlying CGI API, perhaps we 
should be calling this instead. It looks to still be intimately entwined with
UI but that does not make it worse than web scraping.

For example, here is a useful function from /functions.js on the device:

My impression is that it would be harder to specify a call to this function
than it was to 'press' the correct buttons in the UI. However the resulting 
solution would not require Chrome and might be more robust.

.. code-block:: javascript

    function submitPoePortEdit(){
        var hash = $("#hash").val();
        var portId = $("#poePortID").val();
        var portPwr = $("#poePortPwrSelect").val();
        var portPrio = $("#poePortPrioSelect").val();
        var pwrMode = $("#poePwrModeSelect").val();
        var limitType = $("#poePwrLimitTypeSelect").val();
        var limit = $("#poePwrLimit").val();
        var detecType = $("#poeDetecTypeSelect").val();
        var datas = "";

        datas = "hash=" + hash + "&ACTION=Apply" + "&portID=" + (portId - 1) + "&ADMIN_MODE=" + portPwr + "&PORT_PRIO=" + portPrio;
        datas = datas + "&POW_MOD=" + pwrMode + "&POW_LIMT_TYP=" + limitType;
        if ($("#poePwrLimit").prop("disabled")) {
            datas = datas + "&DETEC_TYP=" + detecType;
        }
        else {
            datas = datas + "&POW_LIMT=" + limit + "&DETEC_TYP=" + detecType;
        }

        if (!$("#poePwrLimit").prop("disabled")) {
            if (limitType == 2) {
                if (pwrMode == 0) {
                    if (!(limit >= 3.0 && limit <= 15.4)){
                        toggleModalWindow("alert","ml337","ml371");
                        return false;
                    }
                }
                else {
                    if (!(limit >= 3.0 && limit <= 30.0)){
                        toggleModalWindow("alert","ml337","ml372");
                        return false;
                    }
                }
            }
        }

        footerMsg("Applying");
        $.ajax({
            url: "/PoEPortConfig.cgi",
            type: "POST",
            data: datas,
            dataType: "text",
            success: function(data){
                if (data == "SUCCESS"){
                    footerMsg("Applied");
                }
                else if (data == "CHECK HASH FAILED"){
                    redirectToLoginPage();
                    return;	
                }	            
                else if(data.substring(0,6)=="<html>")
                {
                    $(".footer").css("display", "none");
                }
                else{
                    toggleModalWindow("alert","ml337",data);
                    $(".footer").css("display", "none");
                }
                cancelSettingPage("PoEPortConfig");
            },
            error: function(){
                toggleModalWindow("alert","ml337","ml179");
                }
            }
        );
    }