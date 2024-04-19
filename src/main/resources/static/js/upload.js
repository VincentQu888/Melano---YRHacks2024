function updateImg(event){
    var preview = document.querySelector('img');
    var file = document.querySelector('input[type=file]').files[0];
    var reader = new FileReader();
    
    reader.onloadend = function(){
        preview.src = reader.result;
    }
    
    if(file){
        reader.readAsDataURL(file)
        document.getElementById('input-content').style.display = 'none';
        document.getElementById('preview').style.display = 'block';
        document.getElementById('image-submit-button').style.display = 'block';
    }else{
        preview.src = "";
        document.getElementById('input-content').style.display = 'block';
        document.getElementById('preview').style.display = 'none';
        document.getElementById('image-submit-button').style.display = 'none';
    }
}



var hasFile = document.querySelector('input[type=file]').files[0];
if(!hasFile){
    document.getElementById('image-submit-button').style.display = 'none';
}



function popup(){
    document.getElementById('loading-popup').style.display = 'flex';
    document.getElementById('darkened-overlay').style.display = 'block';
    document.getElementById('image-submit-button').style.display = 'none';
}
