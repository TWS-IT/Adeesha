<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Employee Inventory</title>
  <link rel="stylesheet" href="style.css">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
</head>
<body>
  <nav class="navbar">
    <div class="navbar-brand">Employee Inventory</div>
    <div class="nav-links">
      <a href="/">Add Employee</a>
      <a href="/employees">Employee List</a>
    </div>
  </nav>

  <main class="main-container">
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, msg in messages %}
          <div class="flash-message {{ category }}">{{ msg }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}

    {% block content %}{% endblock %}
  </main>
</body>
</html>
