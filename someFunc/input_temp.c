//if
int_t main()

{
  int i,N,sum = 0,choice=0;
  int i,N,sum = 0,choice=0;
  N = read();
  choice=read();
  if(choice == 1) {
//      for(i=1;i<=N;i=i+1)
//      {
//         if(i%2 == 1)
	    sum = sum+i;
//      }
  }
  if(choice == 2){
//  else if(choice == 2){
      i=0;
      while(i<N){
      sum = sum + i;
      i = i + 2;
     }
   }
  write(sum);
}