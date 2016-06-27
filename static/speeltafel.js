var speeltafel = function(window, document) {
        probeer = function(wie, wat){
            var rq = new window.XMLHttpRequest();
            rq.init = function(){
                    rq.open('POST', '/grijp/'+wie+'/'+wat);
                    rq.send(null);
                };
             rq.onreadystatechange = function(){
                    switch (rq.readyState) {
                        case 4: console.log("DONE, status = " + rq.status); resultaat(rq); break;
                        default: break;
                    }
                };
            rq.init();
        };

        var resultaat = function(rq) {
            var element = document.getElementById("resultaat");
            element.innerHTML = rq.responseText;
        };

        return {
            probeer: probeer,
            resultaat: resultaat
        };
}(window, document);