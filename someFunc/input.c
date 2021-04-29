int a=1;
int test_func (int);
int main (){
    int i = 0, j = 0;
    i = test_func(1);
    if(i == 0){
        int i = 0;
        while(1){
            i = 1;
            i = test_func(1);
        }
    }
    for(i = 0; i < 10; i = i + 1){
        for(j = 0; j < 10; j = j + 1){
            j = j + 1;
        }
        if( i < 10 ){
            i = i + 1 ;
            if (j>5){
                j = j + 2;
            }
        }else{
            const int j = 0;
            break;
        }
    }
    return 0;
}
int test_func (int para){
    int i = 0;
    return 0;
}
