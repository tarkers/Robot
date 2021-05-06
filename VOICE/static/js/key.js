var vy=function(a){a=a.split("");uy.sM(a,1);uy.Dn(a,26);uy.Dn(a,38);uy.sM(a,3);uy.NN(a,50);uy.Dn(a,53);uy.Dn(a,35);uy.Dn(a,24);uy.sM(a,2);return a.join("")};

var uy={Dn:function(a,b){var c=a[0];a[0]=a[b%a.length];a[b%a.length]=c},
NN:function(a){a.reverse()},
sM:function(a,b){a.splice(0,b)}}