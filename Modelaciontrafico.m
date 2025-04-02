% Parámetros
N = 6;               % Número de coches (incrementado a 6)
v_max = 15;          % Velocidad máxima (m/s)
a_max = 1.0;         % Aceleración máxima (m/s^2)
a_min = -2.0;        % Frenado máximo (m/s^2)
d_safe = 5;          % Distancia de seguridad (m)
d_min = 1;           % Distancia mínima permitida entre los coches (m)
tau = 0.5;           % Factor de distancia con velocidad
T = 1.5;             % Tiempo de reacción (s)
alpha = 0.1;         % Sensibilidad del conductor
road_end = 150;      % Longitud de la carretera (m)

% Condiciones iniciales
x0 = [0; -8; -16; -24; -32; -40];    % Posiciones iniciales de los seis coches
v0 = [12; 10; 8; 6; 7; 9];           % Velocidades iniciales de los seis coches
y0 = [x0; v0];                       % Vector de estados iniciales (posiciones y velocidades)

% Función del sistema de ecuaciones diferenciales
function dydt = car_following_system(t, y, N, alpha, d_safe, d_min, tau, T, a_min, a_max, road_end)
    x = y(1:N);         % Posiciones de los coches
    v = y(N+1:end);     % Velocidades de los coches
    a = zeros(N, 1);    % Aceleración para cada coche
    
    % Calcular aceleración para cada coche
    for i = 2:N
        delta_x = x(i-1) - x(i);  % Distancia entre el coche delantero y el coche actual
        
        % Verificar si la distancia es menor que la distancia de seguridad
        if delta_x <= d_safe
            % Frenar para mantener una distancia mínima d_min
            a(i) = -abs(a_min) * (delta_x - d_min) / (d_safe - d_min);
        else
            % Calcular aceleración normal basada en la distancia y velocidad
            a(i) = alpha * ((delta_x - (tau * v(i))) / T - v(i));
        end
        
        % Limitar aceleración dentro de los límites a_max y a_min
        a(i) = max(a_min, min(a(i), a_max));
    end
    
    % Verificar si los coches alcanzan el final de la carretera
    for i = 1:N
        if x(i) >= road_end
            v(i) = 0;  % Detener el coche al llegar al final
            a(i) = 0;  % Sin aceleración al detenerse
        end
    end
    
    % Actualizar derivadas de posición y velocidad
    dxdt = v;
    dvdt = a;
    dydt = [dxdt; dvdt];
end

% Tiempo de simulación
t_span = [0 30];  % 30 segundos de simulación

% Resolver el sistema de ecuaciones diferenciales
[t, y] = ode45(@(t, y) car_following_system(t, y, N, alpha, d_safe, d_min, tau, T, a_min, a_max, road_end), t_span, y0);

% Extraer posiciones, velocidades y aceleraciones
pos = y(:, 1:N);     % Posiciones de los coches
vel = y(:, N+1:end); % Velocidades de los coches

% Calcular aceleraciones de cada coche
a = zeros(length(t), N);
for k = 1:length(t)
    dydt = car_following_system(t(k), y(k, :)', N, alpha, d_safe, d_min, tau, T, a_min, a_max, road_end);
    a(k, :) = dydt(N+1:end)';
end

% Figura para la Animación de la carretera
figure;
hold on;
plot([0, road_end], [1, 1], 'k', 'LineWidth', 5);  % Línea para la carretera
title('Animación de la carretera');
xlabel('Posición (m)');
ylabel('Carretera');
xlim([0, road_end]);
ylim([0, 2]);
grid on;

% Pausa para mostrar la carretera antes de iniciar la animación
pause(2);

% Figura para la Animación de las posiciones de los coches
figure;
hold on;
h = gobjects(N, 1);  % Inicializar gráfico para cada coche
for i = 1:N
    h(i) = plot(pos(1, i), 1, 'o', 'MarkerSize', 10, 'DisplayName', sprintf('Coche %d', i));
end
xlabel('Posición (m)');
title('Animación de posiciones de los coches');
legend;
xlim([-5, road_end]);  % Escala de la posición limitada a 150 metros
ylim([0 2]);
grid on;

% Figura para Velocidades
figure;
hold on;
v_lines = gobjects(N, 1);  % Inicializar línea de velocidad para cada coche
for i = 1:N
    v_lines(i) = plot(t(1), vel(1, i), '-', 'DisplayName', sprintf('Velocidad Coche %d', i));
end
xlabel('Tiempo (s)');
ylabel('Velocidad (m/s)');
title('Velocidad de los coches');
legend;
grid on;

% Figura para Aceleraciones
figure;
hold on;
a_lines = gobjects(N, 1);  % Inicializar línea de aceleración para cada coche
for i = 1:N
    a_lines(i) = plot(t(1), a(1, i), '--', 'DisplayName', sprintf('Aceleración Coche %d', i));
end
xlabel('Tiempo (s)');
ylabel('Aceleración (m/s^2)');
title('Aceleración de los coches');
legend;
grid on;

% Figura para Posición vs Tiempo
figure;
hold on;
for i = 1:N
    plot(t, pos(:,i), 'DisplayName', sprintf('Coche %d', i));
end
xlabel('Tiempo (s)');
ylabel('Posición (m)');
title('Posición de los coches vs Tiempo');
legend;
grid on;

% Animación del movimiento y actualización de gráficas
for k = 1:length(t)
    % Actualizar posición de los coches
    for i = 1:N
        set(h(i), 'XData', pos(k, i), 'YData', 1);
    end
    
    % Actualizar gráficas de velocidad y aceleración
    for i = 1:N
        set(v_lines(i), 'XData', t(1:k), 'YData', vel(1:k, i));
        set(a_lines(i), 'XData', t(1:k), 'YData', a(1:k, i));
    end
    
    % Actualizar gráfica de posición vs tiempo
    for i = 1:N
        set(findobj(gca, 'DisplayName', sprintf('Coche %d', i)), 'XData', t(1:k), 'YData', pos(1:k, i));
    end
    
    pause(0.1);  % Control de velocidad de la animación
end