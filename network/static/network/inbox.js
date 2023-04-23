document.addEventListener('DOMContentLoaded', function() {


    document.addEventListener('click', event => {
        const element = event.target;
        if (element.className === 'Edite'){
            var CC = document.querySelector(`#a${element.id}`).textContent;
            const i = element.id;
            Edite(CC,i);
        }

        if (element.className === 'Like'){
            const i = element.id;
            fetch(`/like`, {
                method: 'POST',
                body: JSON.stringify({
                    id : i
                    
                })
            })
            const a = document.getElementById(`c-${i}`);
            if (a === null ){
                var y = document.querySelector(`#l-${i}`).textContent;
                
                var z = parseInt(y);
                if(element.innerText !== "Unlike"){
                    document.querySelector(`#l-${i}`).innerHTML = "";
                    document.querySelector(`#l-${i}`).innerHTML = `${z+1}`;
                    element.innerText = "Unlike";
                }
                else{
                
                    document.querySelector(`#l-${i}`).innerHTML = "";
                    document.querySelector(`#l-${i}`).innerHTML = `${z-1}`;               
                    element.innerText = "Like";
                
                }
            }
            else {
                var y = document.querySelector(`#l-${i}`).textContent;
                
                var z = parseInt(y);
                if(element.innerText === "Unlike"){
                    document.querySelector(`#l-${i}`).innerHTML = "";
                    document.querySelector(`#l-${i}`).innerHTML = `${z-1}`;
                    element.innerText = "Like";
                }
                else{
                    document.querySelector(`#l-${i}`).innerHTML = "";
                    document.querySelector(`#l-${i}`).innerHTML = `${z+1}`;
                    element.innerText = "Unlike";
                }
                
            }
        


        }



    });

    

});



function Edite(c,i){
    document.querySelector('#Content').style.display = 'none';
    document.querySelector('#edite').style.display = 'block';
    document.querySelector('#e-content').innerHTML = `${c}`;

    document.querySelector('#s-edite').addEventListener('click', function(){
        const x = document.querySelector('#e-content').value;

        fetch('/edite', {
            method: 'POST',
            body: JSON.stringify({
                body: x,
                id : i
            })
        })
        .then(response =>response.json())
        .then(result => {

        });

    });
}
