from flask import Flask, render_template, request
from data.customers import customers
from data.queues import queues

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        account_number = request.form["account"]
        support_type = request.form["support_type"]

        # Customer Lookup
        customer = customers.get(account_number)

        if not customer:
            return """
            <h2>Customer Not Found</h2>
            <a href="/">Try Again</a>
            """

        # Routing Logic
        selected_queue = queues[support_type]

        # Check for Available Agent
        assigned_agent = None

        for agent in selected_queue["agents"]:
            if agent["available"]:
                assigned_agent = agent["name"]
                break

        customer_name = customer["name"]
        customer_service = customer["service"]

        # No Agent Available
        if assigned_agent is None:
            return render_template(
                "queued.html",
                customer_name = customer_name,
                account_number = account_number,
                customer_service = customer_service,
                queue_name=selected_queue["queue_name"],
                waiting_customers = selected_queue["waiting_customers"]
            )

        # Agent Available
        
        return render_template(
    "result.html",
    customer_name=customer_name,
    account_number=account_number,
    customer_service=customer_service,
    support_type=support_type,
    queue_name=selected_queue["queue_name"],
    assigned_agent=assigned_agent
)
        
    return render_template("index.html")


@app.route("/customer/<account_number>")
def get_customer(account_number):

    if account_number in customers:
        
        return customers[account_number]
    
    return {"error": "Customer not found"}

@app.route("/queues")
def queue_dashboard():

    queue_data = []

    for queue in queues.values():

        available_agents = 0

        for agent in queue["agents"]:
            if agent["available"]:
                available_agents += 1

        queue_data.append({
            "queue_name": queue["queue_name"],
            "waiting_customers": queue["waiting_customers"],
            "available_agents": available_agents
        })

    return render_template(
        "dashboard.html",
        queue_data=queue_data
    )
    
if __name__ == "__main__":
    app.run(debug=True)