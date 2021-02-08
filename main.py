from flask import Flask, Response
import time, chess, json
app = Flask(__name__, static_url_path='/static')
board = chess.Board()



@app.route('/')
def hello():
    return app.send_static_file('index.html')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file("favicon.ico")

@app.route("/move/<move>")
def move(move):
    board.push_san(move)
    return "done"

@app.route("/legalMoves")
def legalMoves():
    movesAsStrings = []
    moves = list(board.legal_moves)
    for move in moves:
        movesAsStrings.append(str(move))
    return json.dumps(movesAsStrings)

@app.route("/reset")
def reset():
    board.reset()
    return "done"

def get_message():
    s = board.fen()
    time.sleep(0.1)
    return s

@app.route('/stream')
def stream():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            yield 'data: {}\n\n'.format(get_message())
    return Response(eventStream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")