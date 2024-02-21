import base64
from io import BytesIO
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

matplotlib.use('agg')  # Fix some weird issue.


def _convert_graph():
    """ Converts the graph to an HTML embeddable. """
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return string.decode('utf-8')


def get_burndown_chart(sprint):
    """ Returns a line chart showing the ideal velocity vs the actual velocity.
    """
    plt.figure(figsize=(10, 6))
    start, end = sprint.start_date, sprint.end_date
    total = sprint.point_progress().total
    # Plot ideal velocity.
    dates = [start + timedelta(days=x) for x in range((end - start).days + 1)]
    points = np.linspace(total, 0, len(dates))
    plt.plot(dates, points, color='blue', label='Ideal Velocity')
    # Style chart.
    plt.title(f"{sprint.name} Burndown Chart")
    plt.xlabel("Date")
    plt.ylabel("Story Points Remaining")
    plt.xticks(dates, labels=[datetime.strftime(d, '%#d/%m') for d in dates])
    # Plot actual velocity.
    dates = [start]
    points = [total]
    for task in sprint.tasks.order_by('due_date'):
        dates.append(task.due_date)
        total -= task.story_points
        points.append(total)
    plt.plot(dates, points, color='red', label='Actual Velocity')
    # Add legend.
    plt.legend()
    # Finally, return the converted graph.
    return _convert_graph()


def get_sprint_vs_log_time_chart(sprints):
    """ Returns a column chart showing the total time spent by the entire team
    on each sprint in the project.
    """
    sprint_name = [sprint.name for sprint in sprints]
    log_times = [sprint.log_time() for sprint in sprints]
    # Create bar chart
    columns = plt.bar(sprint_name, log_times, color='dodgerblue')
    # Add data values
    for col in columns:
        plt.text(x=col.get_x() + col.get_width() / 2,
                 y=col.get_height(),
                 s=str(col.get_height()).replace(".0", ""),
                 ha='center', va='bottom')
    # Add labels
    plt.title("Sprint vs Log Time")
    plt.xlabel("Sprint")
    plt.ylabel("Hours Worked")
    # Adjust margins
    plt.margins(y=0.2)
    # Process graph
    return _convert_graph()


def get_user_vs_log_time_chart(project):
    """ Returns a bar-chart with the time spent by each user on the project.
    """
    names = [user.username for user in project.team]
    log_times = [user.log_time(project) for user in project.team]
    # Create bar chart.
    bars = plt.bar(names, log_times, color='skyblue')
    # Add data labels.
    for bar in bars:
        plt.text(x=bar.get_x() + bar.get_width() / 2,
                 y=bar.get_height(),
                 s=str(bar.get_height()).replace(".0", ""),
                 ha='center', va='bottom')
    # Add titles and axis labels.
    plt.title("User vs Log Time")
    plt.xlabel("Username")
    plt.ylabel("Hours Worked")
    plt.ylim(bottom=0)
    # Adjust margin.
    plt.margins(y=0.2)
    # Finally, return the converted graph.
    return _convert_graph()
