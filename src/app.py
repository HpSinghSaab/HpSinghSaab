from flask import Flask, render_template, request, jsonify
from src.tax_engine.flow_through_calc import FlowThroughCalculator
from src.tax_engine.capital_gains import CapitalGainsCalculator2025
from src.geology.drill_parser import DrillParser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate_tax():
    data = request.json
    try:
        price = float(data.get('price', 1.0))
        investment = float(data.get('investment', 10000.0))
        tax_rate = float(data.get('tax_rate', 0.50))
        province = data.get('province', 'ON')

        calc = FlowThroughCalculator(marginal_tax_rate=tax_rate, province=province)
        result = calc.calculate_breakeven(share_price=price, investment_amount=investment)

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/capgains', methods=['POST'])
def calculate_capgains():
    data = request.json
    try:
        gain = float(data.get('gain', 0.0))
        tax_rate = float(data.get('tax_rate', 0.50))
        entity = data.get('entity', 'Individual')

        calc = CapitalGainsCalculator2025(marginal_tax_rate=tax_rate, entity_type=entity)
        result = calc.calculate_tax(gain)

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/parse', methods=['POST'])
def parse_drill():
    data = request.json
    text = data.get('text', '')

    parser = DrillParser()
    results = parser.parse_text(text)

    # Calculate Au equivalent score (just Au for now)
    score = parser.calculate_metal_content(results, target_element="Au")

    return jsonify({
        'intercepts': results,
        'au_gram_meters': score
    })

if __name__ == '__main__':
    app.run(debug=False, port=5000)
