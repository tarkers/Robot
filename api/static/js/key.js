var vy=function(a){a=a.split("");uy.bH(a,3);uy.Fg(a,7);uy.Fg(a,50);uy.S6(a,71);uy.bH(a,2);uy.S6(a,80);uy.Fg(a,38);return a.join("")};

var uy={bH:function(a,b){a.splice(0,b)},
Fg:function(a,b){var c=a[0];a[0]=a[b%a.length];a[b%a.length]=c},
S6:function(a){a.reverse()}}