/* Active mover Simulation(Drive equ+52883

ment)) */

//Good work

/*** define macro ***/
//Motor spec
MOTOR_RESOLUTION = 1000;    //ステッピングモータ分解能
GEAR_RATIO = 50;    //ギア比
SAMPLING = 1000;
RESOLUTION = MOTOR_RESOLUTION * GEAR_RATIO / SAMPLING; //正味分解能

ALPHA = 90; //[deg]    90
H_lar = 0;  //z offset  77
R = 20;    //radious of cam
h_sma = 5;  //value of hensin
L = 80;    //distance bitween cams 80

/*** define variable value ***/
pls_num1 = 0; //quantity of pulse on cam1(Manipulate)
pls_num2 = 0; //quantity of pulse on cam2(Manipulate)
x_posi = 0; //position at x axi(Control)
z_posi = 0; //position at z axi(Control)
x_posi_pre = 0; //position at x axi(Control)
z_posi_pre = 0; //position at z axi(Control)
theta_deg_1 = 0; //rotate angle on cam1
theta_deg_2 = 0; //rotate angle on cam2
theta_rad_1 = 0; //rotate angle on cam1
theta_rad_2 = 0; //rotate angle on cam2

i=0; j=0;

/*** function ***/
function  rev = PlsToRev(pls);//convert from a number of pulse to revoluton 
    rev = pls / RESOLUTION;
endfunction

function  deg = RevToDeg(rev);//convert from degree to radian
    deg = rev *360;
endfunction

function  rad = DegToRad(deg);//convert from degree to radian
    rad = deg/360 * 2*%pi;
endfunction


for i = 0:RESOLUTION,
    disp(i)
    for j = 0:RESOLUTION,
        pls_num1 = i;
        theta_deg_1 = RevToDeg(PlsToRev(pls_num1)); //rotate angle on cam1
        theta_rad_1 = DegToRad(theta_deg_1); //rotate angle on cam2
        x_1 = tan(ALPHA/2)/2 * h_sma * (sin(theta_rad_1) - sin(theta_rad_2));
        x_2 = (h_sma*(cos(theta_rad_1) + cos(theta_rad_2)) + L)/2
        x_posi = x_1 + x_2;    
        
        pls_num2 = j;
        theta_deg_2 = RevToDeg(PlsToRev(pls_num2)); //rotate angle on cam1
        theta_rad_2 = DegToRad(theta_deg_2); //rotate angle on cam2
        z_1 = R*sin(ALPHA/2) + H_lar;
        z_2 = (sin(theta_rad_1) + sin(theta_rad_2)) * h_sma/2;
        z_3_1 = 2*R*cos(ALPHA/2) + h_sma*cos(theta_rad_1) - h_sma*cos(theta_rad_2) - L;
        z_3_2 = tan(ALPHA/2);
        z_3 = (z_3_1 / z_3_2) /2;
        
        z_posi = z_1 + z_2 + z_3;
    
        plot(x_posi, z_posi,'.')
        strf = "041"
        frameflag=4
    end    
end



time = toc()

xgrid() //←グリッドの表示
xtitle('Range of motion', 'X axi move area', 'Y axi move area')  //←タイトル関連の表示

disp("Finish plotting")

//scf(0);//グラフ02
//plot(t, y)  //←グラフ表示
//xgrid() //←グリッドの表示
///xtitle('Step Responces', 'Time[sec]', 'Amplitude')  //←タイトル関連の表示
