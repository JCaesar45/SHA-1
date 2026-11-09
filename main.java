http.authorizeHttpRequests(registry -> registry
    .requestMatchers("/actuator/health", "/api/public/**").permitAll()
    .requestMatchers("/api/admin/**").hasRole("ADMIN")
    .anyRequest().authenticated()
);
