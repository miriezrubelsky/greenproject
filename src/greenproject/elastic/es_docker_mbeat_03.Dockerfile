FROM docker.elastic.co/beats/metricbeat:7.11.1

# Copy Metricbeat configuration
COPY metricbeat.yml /usr/share/metricbeat/metricbeat.yml

# Copy the startup script
COPY startup.sh /usr/share/metricbeat/startup.sh

# Change permissions to ensure the script is executable
RUN chmod +x /usr/share/metricbeat/startup.sh

USER root
RUN chown root /usr/share/metricbeat/metricbeat.yml

# Set the startup script as the entry point
ENTRYPOINT ["/usr/share/metricbeat/startup.sh"]