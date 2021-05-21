int_t main (){
    int i=1+2+3;
    while(i>0){
        i = 1;
    }
    if (i==0){
        i=2;
        if (i==2){
            int j=0;
            i=3;
        }else{
            i=4;
        }
    }else{
        i=6;
    }
    return 0;
}
