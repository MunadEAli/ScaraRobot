function envelop()
    a1 = 0.14553;
    a2 = 0.250;
    a3 = 0.15275;
    h1 = 0.059;
    d3 = 0.086;
    d4 = 0.114;

    Q1 = linspace(0, 0.195, 50);
    Q2 = linspace(-150, 150, 100) * pi / 180;  % Convert to radians
    Q3 = linspace(-150, 150, 100) * pi / 180;  % Convert to radians

    % Preallocate arrays for the coordinates
    num_points = length(Q1) * length(Q2) * length(Q3);
    x = zeros(num_points, 1);
    y = zeros(num_points, 1);
    z = zeros(num_points, 1);

    % Index for preallocated arrays
    idx = 1;

    % Iterate over Q1, Q2, and Q3
    for i = 1:length(Q1)
        for j = 1:length(Q2)
            for k = 1:length(Q3)
                % Calculate x, y, z for each combination of Q1, Q2, and Q3
                x(idx) = a1 + a2 * cos(Q2(j)) + a3 * cos(Q2(j) + Q3(k));
                y(idx) = -a2 * sin(Q2(j)) - a3 * sin(Q2(j) + Q3(k));
                z(idx) = Q1(i) - d3 - d4 + h1;

                % Increment index
                idx = idx + 1;
            end
        end
    end

    % Calculate the convex hull
    K = convhull(x, y, z);

    % Get the points on the convex hull
    hull_points = unique(K);

    % Extract the coordinates of the hull points
    x_hull = x(hull_points);
    y_hull = y(hull_points);
    z_hull = z(hull_points);

    % Create a figure for 3D plot
    figure;
    hold on;

    % Plot the convex hull points
    plot3(x_hull, y_hull, z_hull, 'bo', 'MarkerFaceColor', 'b');

    % Plot the convex hull as a surface for better visualization
    trisurf(K, x, y, z, 'FaceColor', 'green', 'FaceAlpha', 0.3, 'EdgeColor', 'none');

    % Set axis labels
    xlabel('X');
    ylabel('Y');
    zlabel('Z');

    % Set the title
    title('3D Working Envelope of SCARA Robot');

    % Enable grid
    grid on;

    % Hold off to stop adding to the current plot
    hold off;

    % Improve visualization
    camlight;
    lighting gouraud;
    axis equal;
end
