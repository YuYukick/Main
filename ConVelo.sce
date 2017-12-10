disp("Start plotting")
h_sma = 5;

sample_data = 100;
resolution = 2*%pi / sample_data;
resolution_2 = 1 / sample_data;

x_posi = 0;
x=0;

scf(0)
clf()
for j = 0:sample_data,
    disp(j);
    x_posi = h_sma * cos(resolution * j);
             
    plot(resolution*j, x_posi,'.')
    strf = "041"
    //frameflag=4
end    
xgrid() //←グリッドの表示
xtitle('Range of motion', 'X axi move area', 'Y axi move area')  //←タイトル関連の表示
xs2png(0,'fig1.png');

scf(1)
clf()
// x 初期化
x=[0:0.1:2*%pi]';
plot(x,cos(x))
xs2png(0,'fig2.png');

disp("Finish plotting")

scf(2)
clf()
for j = 0:sample_data,
    disp(j);
    x_posi = -acos(resolution_2 * j);
             
    plot(resolution_2*j, x_posi,'.')
    strf = "041"
    //frameflag=4
end
for j = 0:sample_data,
    disp(j);
    x_posi = -acos(-resolution_2 * j);
             
    plot(-resolution_2*j, x_posi,'.')
    strf = "041"
    //frameflag=4
end    
xgrid() //←グリッドの表示
xtitle('Range of motion', 'X axi move area', 'Y axi move area')  //←タイトル関連の表示


scf(3)
clf()
sample_data = sample_data;
for i = 1:5,
    disp(i);
    for j = 0:sample_data,
        disp(j);
        x_posi = -h_sma *cos(acos(-resolution_2 * j));
                 
        plot(-resolution_2*j+(4*i-1), x_posi,'.')
        strf = "041"
        //frameflag=4
    end 
    for j = 0:sample_data,
        disp(j);
        x_posi = -h_sma *cos(acos(resolution_2 * j));
                 
        plot(resolution_2*j+(4*i-1), x_posi,'.')
        strf = "041"
        //frameflag=4
    end
    for j = 0:sample_data,
        disp(j);
        x_posi = h_sma *cos(acos(-resolution_2 * j));
                 
        plot(-resolution_2*j + (4*i+1), x_posi,'.')
        strf = "041"
        //frameflag=4
    end
    for j = 0:sample_data,
        disp(j);
        x_posi = h_sma *cos(acos(resolution_2 * j));
                 
        plot(resolution_2*j+ (4*i+1), x_posi,'.')
        strf = "041"
        //frameflag=4
    end
end
xgrid() //←グリッドの表示
xtitle('Range of motion', 'X axi move area', 'Y axi move area')  //←タイトル関連の表示
