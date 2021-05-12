int_t main (){
    for(i = 0; i < 10; i = i + 1){
        for(j = 0; j < 10; j = j + 1){
            j = j + 1;
        }
        if( i < 10 )
        {
            i = i + 1 ;
            if (j>5)
            {
                j = j + 2;
            }
        }
        else
        {
            if (j>5)
            {
                j = j + 2;
            }
            const int j = 0;
            break;
        }
    }
    return 0;
}
