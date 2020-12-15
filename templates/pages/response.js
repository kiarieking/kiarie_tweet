const xhr = new XMLHttpRequest()
const method = 'GET'
const responseType = 'json'
const url = '/tweets'

xhr.responseType = responseType
xhr.onload(method,url)=function(){
    const serveresponse = xhr.response
    var listeditems = serveresponse.response
}
xhr.send()