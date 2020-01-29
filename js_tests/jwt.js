var urlParams = new URLSearchParams(window.location.search)
var code = urlParams.get("code")
var state = urlParams.get("state")

var google_options = {
    client_id: "643017558290-r4ksamj17opnug9gktl3fvmu31pg7b2p.apps.googleusercontent.com",
    client_secret : "kUEQBlNvrUQY8PTG7rug6NlM",
    state : "google",
    response_type: "code",
    response_mode: "query",
    scope: "openid email",
    redirect_uri: "http://localhost:5500",
    nonce: "nonce",
    grant_type: "authorization_code"
}

var google_jwt_authorize = () => {
    var authorize_url = `https://accounts.google.com/o/oauth2/v2/auth?response_type=${google_options.response_type}&client_id=${google_options.client_id}&redirect_uri=${google_options.redirect_uri}&state=${google_options.state}&nonce=${google_options.nonce}&scope=${google_options.scope}`
    window.location.href=authorize_url   
}

var google_jwt_token = async () => {

            var token_url = "https://oauth2.googleapis.com/token"
            var data = {
                code: code,
                client_id: google_options.client_id,
                client_secret: google_options.client_secret,
                redirect_uri: google_options.redirect_uri,
                grant_type: google_options.grant_type
            }
            var formBody = Object.keys(data).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(data[key])).join('&')
            var res = await fetch(token_url, {
                method:"POST",
                mode:"cors",
                body: formBody,
                headers:{"Content-Type":"application/x-www-form-urlencoded"}
            })
            var resp = await res.json()
            console.log(resp)
            document.getElementById("id_token").innerText = resp.id_token

}

var microsoft_options = {
    client_id: "12c3f283-1ab1-4a03-87d9-b8b0d3da77ce",
    client_secret : "d-vevH2j5y:oDKGh=2U]1INNJL=Td=lt",
    state : "microsoft",
    response_type: "code",
    response_mode: "query",
    scope: "openid",
    redirect_uri: "http://localhost:5500",
    nonce: "nonce",
    grant_type: "authorization_code",
    code_challenge: "XbnSsQzdIWdwzgE2Zdk4htkcIU0rQ9rmH80TcUdWzac",
    code_verifier: "TlAcxnped23T0S6VLOWHu3WpsFnWW68ua3FRYZ6h3LPTcYmn2AQedkTfRjNyEfwP2kggiSVMSSipdjAW6TFdmeoMgOQMDDo0h2SkLPAHSajv52T7EOa0aHydbEYVUsqt"
}


var microsoft_jwt_authorize = () => {
    var authorize_url = `https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=${microsoft_options.response_type}&response_mode=${microsoft_options.response_mode}&client_id=${microsoft_options.client_id}&redirect_uri=${microsoft_options.redirect_uri}&state=${microsoft_options.state}&nonce=${microsoft_options.nonce}&scope=${microsoft_options.scope}&code_challenge=${microsoft_options.code_challenge}&code_challenge_method=S256`
    window.location.href=authorize_url   
}

var microsoft_jwt_token = async () => {

    var token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    var data = {
        code: code,
        client_id: microsoft_options.client_id,
        client_secret: microsoft_options.client_secret,
        redirect_uri: microsoft_options.redirect_uri,
        grant_type: microsoft_options.grant_type,
        code_verifier: microsoft_options.code_verifier
    }
    var formBody = Object.keys(data).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(data[key])).join('&')
    var res = await fetch(token_url, {
        method:"POST",
        body: formBody,
        mode: "cors",
        credentials: "include",
        headers:{"Content-Type":"application/x-www-form-urlencoded"}
    })
    var resp = await res.json()
    console.log(resp)
    document.getElementById("id_token").innerText = resp.id_token

}

switch(state){
    case "google":
        google_jwt_token()
    case "microsoft":
        microsoft_jwt_token()
        window.alert("Token will only be shown in the network logs")
    
    window.history.replaceState("", "Get Jwt", "http://localhost:5500")
}