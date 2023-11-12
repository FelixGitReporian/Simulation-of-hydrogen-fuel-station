classdef (ConstructOnLoad) Tank < handle
     %% Properties hydrogen
     properties (Access=protected)
         % General hydrogen properties
         Tc = 33.19; %K, critical temperature
         Pc = 13.13*10^5; %Pa, critical pressure
         Mr = 2.016*10^-3; %kg/mol,molar mass
         R = 8.314; %J/(K*mol,gas constant
         % Redlich Kwong (RK) EoS - Parameters
         a = 0.1428; %m^6*Pa*K^0.5/mol^2 --> a=0.42748*R^2*Tc^2.5/Pc
         b = 1.8208e-05; %m^3/mol --> b=0.08664*R*Tc/Pc
        
         %Thermodynamic properties of hydrogen
         v; %m3/mol, molar volume: v=V*Mr/m
         v_ref; %m3/mol, molar volume: Calculated at a
         % reference state (NWR,15°C). Used for SOC calculation
         u; %J/mol, inner energy
         cp = 28.64; %J/(mol*K),specific heat capacity of hydrogen @300 K
         cv = 20.34; %J/(mol*K),specific heat capacity of hydrogen @300 K
         T_afterThrottle; %K,Temperatur of hydrogen after its
         % expansion (before entering a tank)
        
         % Properties at a reference state (Olmos et al. 2013)
         uref=5132.9; %J/mol
         href=7721.6; %J/mol
         Tref=286.64; %K
         pref=138.07*10^5; %Pa
         vref=1.8958*10^-4; %m^3/mol
        
         %Point of time
         timestep=0; %point of time
     end
    
     %% Open properties of the tank and the hydrogen state in the tank
     properties (SetAccess=private)
         %Standard properties of each tank
         A_tank_out=1.1; %m2,externl surface area of the tank
         A_tank_in=1.1; %m2,inner surface area of the tank
         c_in; %J/(kg*K),specific heat capacity of the inner material
         c_out; %J/(kg*K),specific heat capacity of the outer material
         m_in; %kg,effective mass of the inner material
         m_out; %kg,effective mass of the outer material
         a_gas; %W/(m2*K) convection heat transfer coefficient from the 
         % gas to the inner material
         a_amb; %W/(m2*K) convection heat transfer coefficient from the 
         % outer material to the environment
         V=1; %m3,volume. Calculated with RK --> V=v*n=v*Mr/m
         p_max=50e5; %Pa,maximum allowed pressure of the tank
         p_threshold=100e5 %Pa,minimum allowed pressure in the tank
         m_max=5; %kg,maximum stored mass
         T_max=358.15; %K,maximum allowed temperature in the tank
         T_ref_storage=288.15; %K,reference temperature at which maximum mass is 
         % calculated (SAEJ2601: T_ref_storage=15°C)
         T_wall=293.15; %K,temperature of the wall of the tank
         
        
         % State of hydroegen in the tank
         p = 20e5; %Pa,pressure
         
         m = 2; %kg,mass
         SOC; %state of charge (%)
     end
     properties (Access=public)
         T_amb;
         T = 273.15; %K,temperature
    
     end
    
     %% Methods
     methods
         %% Definition of the tanks
         function obj = Tank(p_max,p_threshold,m_max,m_start,T_amb,A_tank_in, A_tank_out,c_in,c_out,m_in,m_out,a_gas,a_amb)
             obj.A_tank_out=A_tank_out;
             obj.A_tank_in=A_tank_in;
             obj.c_in=c_in;
             obj.c_out=c_out;
             obj.m_in=m_in;
             obj.m_out=m_out;
             obj.V=obj.calc_v(p_max,obj.T_ref_storage)*m_max/obj.Mr;
             obj.p_max = p_max;
             obj.p_threshold=p_threshold;
             obj.m_max = m_max;
             obj.T_amb=T_amb;
             obj.T = obj.T_amb;
             obj.T_wall = obj.T_amb;
             obj.m=m_start;
             obj.a_gas=a_gas;
             obj.a_amb=a_amb;
             obj.update(0);
         end
         %% Function for discharging the tank
         function [m_fuel,T_fuel,p_fuel,m_tank] = discharge(obj,mout,timestep)
             m_fuel=mout; %kg/s,mass flowing out of a tank
             p_fuel=obj.p; %Pa,pressure of mout, equal to the pressure of the 
             %disp(p_fuel)
             % tank in the previous step
             T_fuel=obj.T; %K,temperatur of mout, equal to the temperature of the 
             % tank in the previous step
             hout = obj.calc_h(obj.v,obj.T,obj.p); %J/mol,enthalpy ofthe mout. 
             % Calculated according to the properties of the hydrogen in the tank
             obj.m = obj.m - mout; %kg,new mass in thetank after mout has been removed. 
             % Calculated every second
             m_tank=obj.m;
             obj.update(timestep); %update mass of the tank and consequently p,SOC. T 
             % is not updated in this step
             %Calculation of the temperature change in the tank because of the removed 
             % mass using energy balace equation in the tank
             dudT=(-log(obj.v/(obj.v+obj.b))*(3*obj.a/(4*obj.b*obj.T^1.5)))+ (obj.cp-obj.R); %J/(mol*K)
             dudv=(3*obj.a/(2*obj.T^0.5))*(1/((obj.v+obj.b)*obj.v)); %J/m3
             dvdt=(obj.V*obj.Mr*mout)/(obj.m^2); %m3/mol*s
             dTdt=(((mout/obj.m)*(-hout+obj.u))-(dudv*dvdt))/(dudT);
             obj.T = obj.T + dTdt; %K,new T of tank
             %obj.update(timestep); %update T along with p
         end
    
         %% Function for charging the tank
    
         function [m_tank,T_tank,p_tank,T_in,q_cooling] = charge(obj,m_in,T_source, p_source,T_cooling,timestep)
             %1st step: Check if the source tank that has been chosen has enough
             %pressure to fill the target tank
            
             if p_source < obj.p
                disp('Charging not possible!');
             end
            
             %2nd step: hydrogen is being cooled down to a target 
             % temperature(T_cooling) at heat exchanger (HEX), before entering the
             % target tank
             %The cooling power of the HEX is calculated as follows:
            
             Q_cooling=(obj.cp/obj.Mr)*(T_source-T_cooling)*10^-3; %kJ/kg
             q_cooling=Q_cooling*m_in; %kW
            
             %We assume that hydrogen is cooled isobaric. Therefore there is no
             %pressure loss because of the cooling.
            
             p_cooled = p_source;
            
             %3rd step: H2 passes through the nozzle end expands at the pressure of 
             % the target tank. Its temperature rised because the JTE
             p_afterThrottle = obj.p;
             obj.T_afterThrottle = obj.calc_T_JTE(T_cooling,p_cooled);
            
             %4th step: Calculation of the properties of m_in after the expansion:
            
             v_in=obj.calc_v(p_afterThrottle,obj.T_afterThrottle);
            
             h_in=obj.calc_h(v_in,obj.T_afterThrottle,p_afterThrottle);
             %5th step: Every amount of mass per timestep enters the target tan and 
             % its properties are updated
             obj.m=obj.m+m_in;
             %disp(obj.m)
             obj.update(timestep);
             %During this update v is updated because the mass has changed. p is also 
             % updated but using the old temperature because in order to
             % calculate the temperaure rise v is necessary first;
             obj.cp = obj.calc_cp(obj.v,obj.T);
             obj.cv= obj.calc_cv(obj.v,obj.T);
             dudT=(-log(obj.v/(obj.v+obj.b))*(3*obj.a/(4*obj.b*obj.T^1.5))) + obj.cv;
             %J/(mol*K)
             dudv=(3*obj.a/(2*obj.T^0.5))*(1/((obj.v+obj.b)*obj.v)); %J/m3
             dvdt=(-obj.V*obj.Mr*m_in)/(obj.m^2); %m3/(mol*s)
             dTdt=(((m_in/obj.m)*(h_in-obj.u))-(dudv*dvdt))/dudT;
             obj.T = obj.T + dTdt;
             % obj.update(timestep); % v is already adjusted but p needs to be 
             % calculated again, using the "new" T
             % obj.update_T(timestep);
             %At the end of the charging process the new properties of the target
             %tank:
             m_tank=obj.m;
             T_tank=obj.T;
             p_tank=obj.p;
             %disp(p_tank)
             T_in=obj.T_afterThrottle; %Temperature of m_in after the expansion
        
         end
    
         %% Function that is called in order to update the tank properties 
         % after every change
         function [] = update(obj,timestep)
        
             obj.timestep=timestep;
            
             al=obj.a;
             bl=obj.b;
             Rl=obj.R;
             Mrl=obj.Mr;
             T_ref_storagel=obj.T_ref_storage;
             obj.v = obj.V*Mrl/obj.m;
             obj.v_ref=obj.calc_v(obj.p_max,T_ref_storagel);
             obj.SOC = (obj.v_ref/obj.v)*100; %Calculation according 
             % to SAE J2601 § 4.12 Eq.(1) pg.10
             if obj.SOC>120 %SOC is allowed to reach a higher value than 100%
                 % when p_target has not been reached
                disp('mass exceeds limits')
             end
             obj.p =((Rl*obj.T)/(obj.v-bl) - al./(((obj.T^0.5)*obj.v).*(obj.v+bl)));
             obj.u = obj.calc_u(obj.v,obj.T);
             obj.cv=obj.calc_cv(obj.v,obj.T);
         end
    
         function [] = update_T(obj,timestep)
        
             obj.timestep=timestep;
            
             al=obj.a;
             bl=obj.b;
             Mrl=obj.Mr;
            
             dudT=(-log(obj.v/(obj.v+bl))*(3*al/(4*bl*obj.T^1.5))) + obj.cv; %J/(mol*K)
             Q_cond=obj.calc_Q_cond(); %J/s
             q=Q_cond/obj.m; %J/(kg*s)
             obj.T=obj.T-(q/(dudT/Mrl));
            
         end
    
         %% Convection
         function Q_cond=calc_Q_cond(obj)
             dTdtw=(obj.a_gas*obj.A_tank_in*(obj.T- obj.T_wall)- obj.a_amb*obj.A_tank_out*( obj.T_wall-obj.T_amb))/(obj.m_in*obj.c_in+obj.m_out*obj.c_out);
             obj.T_wall=obj.T_wall+dTdtw;
             Q_cond=obj.a_gas*obj.A_tank_in*(obj.T-obj.T_wall); %J/s
            
        
         end
         %% Function for the calculation of T rise because of Joule Thomson Effect
         function [T_JTE] = calc_T_JTE(obj,T_source,p_source)
             % Properties of hydrogen before the throttling valve
             v_source=obj.calc_v(p_source,T_source);
             u_source=obj.calc_u(v_source,T_source);
             h_source=u_source+(p_source*v_source) - (obj.uref + obj.pref*obj.vref) + obj.href;
             % Properties of hydrogen after the throttling valve
             T_JTE=T_source; %initial value for the calculation of the T after 
             % the throt.valve
             t_add=2; %addition in the value of initial temperature
             h_throttle=0; %initial value for the enthalpy of H2 after the valve
             tolerance=100; %h_source~=h_throttle
             while h_throttle<h_source-tolerance || h_throttle>h_source+tolerance
                T_JTE=T_JTE+t_add;
                v_throttle=obj.calc_v(obj.p,T_JTE);
                u_throttle=obj.calc_u(v_throttle,T_JTE);
                h_throttle=u_throttle+(obj.p*v_throttle) - (obj.uref + obj.pref*obj.vref) + obj.href;%calc_h(obj.p,T_throttle);
                if h_throttle>h_source-tolerance
                    break
                end
             end
         end
    
    
         %% Calculation of the thermodynamic properties of hydrogen
         %% Calculation of the molar volume in m^3/mol
         function [v] = calc_v(obj,p,T)
             if p < 10^5
                warning 'type p in Pa!'
             end
             format short
             al=obj.a;
             bl=obj.b;
             Rl=obj.R;
            
             v0 = 10e-4; %initial value for the iteration
             for k = 1:3
                v = (Rl*T/(p+(al/(T^0.5*v0*(v0+bl)))))+bl;
                v0 = v;
             end
         end
         %% Calculation of the molar internal energy in J/mol
         function [u] = calc_u(obj,v,T)
             al=obj.a;
             bl=obj.b;
             Rl=obj.R;
             Trefl=obj.Tref;
             vrefl=obj.vref;
             urefl=obj.uref;
            
             I = (16.9146-Rl)*(T-Trefl) + (1/2)* 8.6356*10^-2 *(T^2-Trefl^2) + (1/3)*(-2.0326*10^-4)*(T^3-Trefl^3) + (1/4)* 1.6016*10^-7*(T^4-Trefl^4); %J/mol
             u = ((log(v)-log(v+bl))*(3*al))/(2*bl*(T^(1/2)))-((log(vrefl)-log(vrefl+bl))*(3*al))/(2*obj.b*(Trefl^(1/2))) + I +urefl; %J/mol
         end
         %% Calculation of the ideal specific heat capacity in J/(molK)
         function [cp] = calc_cp(obj,v,T)
             al=obj.a;
             bl=obj.b;
             Rl=obj.R;
             cp = (Rl*bl/(v-bl))+(al/(2*T^(3/2)*(v+bl)))+ (-3*al/(4*bl*(T^(3/2))))*(log(v)-log(v+bl)) + 16.9146 + 8.6356*10^-2 *(T) - 2.0326*10^-4*(T^2) + 1.6016*10^-7 * (T^3); %J/molK
         end
         %% Calculation of the ideal specific heat capacity in J/(molK)
         function [cv] = calc_cv(obj,v,T)
             al=obj.a;
             bl=obj.b;
             Rl=obj.R;
             cv = (-3*al/(4*bl*(T^(3/2))))*(log(v)-log(v+bl)) + 16.9146+ 8.6356*10^-2 * (T) - 2.0326*10^-4*(T^2) + 1.6016*10^-7 * (T^3) - Rl;
        %J/molK
         end
         %% Calculation of the molar enthalpy in J/mol
         function [h] = calc_h(obj,v,T,p)
             u_temp = obj.calc_u(v,T);
             prefl=obj.pref;
             vrefl=obj.vref;
             hrefl=obj.href;
             h = u_temp +(p*v) - (obj.uref + prefl*vrefl) + hrefl;%J/mol
         end
     end
end