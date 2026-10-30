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

            return f"""
            <h2>Customer Placed In Queue</h2>

            <h3>Customer Information</h3>

            <p><strong>Name:</strong> {customer_name}</p>
            <p><strong>Account Number:</strong> {account_number}</p>
            <p><strong>Current Service:</strong> {customer_service}</p>

            <hr>

            <h3>Queue Details</h3>

            <p><strong>Queue:</strong> {selected_queue['queue_name']}</p>

            <p>
            No agents are currently available.
            Your request has been placed in the queue.
            </p>

            <p>
            <strong>Customers Waiting:</strong>
            {selected_queue['waiting_customers']}
            </p>

            <a href="/">Submit Another Request</a>
            """

        # Agent Available
        return f"""
        <h2>Request Successfully Routed</h2>

        <h3>Customer Information</h3>

        <p><strong>Name:</strong> {customer_name}</p>
        <p><strong>Account Number:</strong> {account_number}</p>
        <p><strong>Current Service:</strong> {customer_service}</p>

        <hr>

        <h3>Routing Details</h3>

        <p><strong>Support Type:</strong> {support_type}</p>

        <p><strong>Assigned Queue:</strong> {selected_queue['queue_name']}</p>

        <p><strong>Assigned Agent:</strong> {assigned_agent}</p>

        <p>
        This request was routed to the
        {selected_queue['queue_name']}
        because the customer selected
        {support_type}.
        </p>

        <a href="/">Submit Another Request</a>
        """

    return render_template("index.html")


@app.route("/customer/<account_number>")
def get_customer(account_number):

    if account_number in customers:
        
        return customers[account_number]
    
    return {"error": "Customer not found"}


if __name__ == "__main__":
    app.run(debug=True)