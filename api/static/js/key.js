var wy=function(a){a=a.split("");vy.PW(a,2);vy.Jq(a,45);vy.Jq(a,38);vy.PW(a,2);vy.Zf(a,31);vy.PW(a,2);return a.join("")};

var vy={PW:function(a,b){a.splice(0,b)},
Jq:function(a,b){var c=a[0];a[0]=a[b%a.length];a[b%a.length]=c},
Zf:function(a){a.reverse()}}