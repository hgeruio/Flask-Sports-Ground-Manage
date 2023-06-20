window.onload=function (){
        document.getElementById('addOk').onclick=function (){
            let email=document.getElementById('email')
            let password1=document.getElementById('password1')
            let password2=document.getElementById('password2')
            let password3=document.getElementById('password3')
            if(password2.value ===password1.value){
            alert("新密码不能与旧密码一致！")
        }else if(password3.value !==password3.value){
            alert("两次密码不同,请重新输入！")
        }else if(email.style.border!=='red 1px solid' && password2.style.border!=='red 1px solid' && password3.style.border!=='red 1px solid'){
            alert("密码修改成功！")
        }
    }
}