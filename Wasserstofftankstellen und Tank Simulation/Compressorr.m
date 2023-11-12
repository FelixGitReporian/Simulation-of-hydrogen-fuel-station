classdef (ConstructOnLoad) Compressorr <handle
     %UNTITLED2 Summary of this class goes here
     % Detailed explanation goes here
    
     properties (Access=protected)
         R = 8.314; %J/(K*mol)
         Mr = 2.016*10^-3; %kg/mol
         R_H2 = 4.124; %kJ/(K*kg)
        
         % Redlich Kwong (RK) EoS - Parameters
         a = 0.1428; %m^6*Pa*K^0.5/mol^2 --> a=0.42748*R^2*Tc^2.5/Pc
         b = 1.8208e-05; %m^3/mol --> b=0.08664*R*Tc/Pc
         % Properties at a reference state (Olmos et al. 2013)
         uref=5132.9; %J/mol
         href=7721.6; %J/mol
         Tref=286.64; %K
         pref=138.07*10^5; %Pa
         vref=1.8958*10^-4; %m^3/mol
     end

     properties (SetAccess=private)
         n=1.4; %polytropic exponent
         NS=1; %Number of stages
         eta_mech=0.75; %mechanischer Wirkungsgrad
         eta_el=1; %elektrischer Wirkungsgrad
         T_out_max=333.15;%maximum temperature of hydrogen at the exit of the compressor
         m_in_max=0.009; %maximum mass input in kg/s
        
     end


     %% methods
     methods
     %% Constructor
    
         function obj = Compressor (n,eta_mech,eta_el)
             obj.n=n;
             obj.eta_mech=eta_mech;
             obj.eta_el=eta_el;
            
         end


         function [T_out,W_adiabatic_real,W_real] = compress(obj,m_in,T_in,p_in,p_out)
        
             %if m_in>obj.m_in_max
              %  error ('compression not possible')
             %end
            
             T_out=obj.calc_T_out(T_in,p_in,p_out);
            
             w_specific_ad = obj.calc_work (T_in,p_in,p_out)/3600;
            %kWh/kg
             w_sp_real=w_specific_ad/obj.eta_mech;
             W_adiabatic_real = w_sp_real*m_in;
            %kWh %polytropic/adiabatic work
            
             dh=obj.calc_dh(T_in,p_in,T_out,p_out)/3600;
            %kWh/kg
             W_real=dh*m_in;
        
         end

         %% Calculation of T_out
         function [T_out]=calc_T_out (obj,T_in,p_in,p_out)
        
             p_ratio=p_out/p_in;
            
             T_out=T_in*(p_ratio)^((obj.n-1)/obj.n);
            
            % if T_out>obj.T_out_max
            % T_out=obj.T_out_max;
            % end
         end
         %% Calculation of real_gas factor

         function [w] = calc_work (obj,T_in,p_in,p_out)
        
             v_in=obj.calc_v(p_in,T_in)/obj.Mr; %m3/kg
             N=obj.n/(obj.n-1);
             Nexp=(obj.n-1)/obj.n;
             w=10^-3*p_in*v_in*N*((p_out/p_in)^Nexp-1); %kJ/kg
             w = max(0,w);
        
         end


         %%
         function [dh] = calc_dh (obj,T_in,p_in,T_out,p_out)
        
             v_out=obj.calc_v(p_out,T_out); %m3/mol
             v_in=obj.calc_v(p_in,T_in); %m3/mol
            
             h_out=obj.calc_h(v_out,T_out,p_out); %J/mol
             h_in=obj.calc_h(v_in,T_in,p_in); %J/mol
            
             dh=(10^-3)*(h_out-h_in)/obj.Mr; %kJ/kg
            
         end
         %% Calculation of the molar volume in m^3/mol
         function [v] = calc_v(obj,p,T)
             if p < 10^5
                warning 'type p in Pa!'
             end
             format short
             v0 = 10e-4; %initial value for the iteration
             for k = 1:3
                v = (obj.R*T/(p+(obj.a/(T^0.5*v0*(v0+obj.b)))))+obj.b;
                v0 = v;
             end
         end
         %% Calculation of the molar internal energy in J/mol
         function [u] = calc_u(obj,v,T)
             I = (16.9146-obj.R)*(T-obj.Tref) + (1/2)* 8.6356*10^-2*(T^2-obj.Tref^2) + (1/3)*(-2.0326*10^-4)*(T^3-obj.Tref^3) + (1/4)*1.6016*10^-7*(T^4-obj.Tref^4); %J/mol
             u = ((log(v)-log(v+obj.b))*(3*obj.a))/(2*obj.b*(T^(1/2)))-((log(obj.vref)-log(obj.vref+obj.b))*(3*obj.a))/(2*obj.b*(obj.Tref^(1/2))) + I +obj.uref; %J/mol
         end

         %% Calculation of the molar enthalpy in J/mol
         function [h] = calc_h(obj,v,T,p)
             u_temp = obj.calc_u(v,T);
             h = u_temp +(p*v) - (obj.uref + obj.pref*obj.vref) +obj.href; %J/mol
         end
     end
end