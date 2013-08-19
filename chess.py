import pgn

pgn_text = open('Kasparov.pgn').read()
pgn_game = pgn.PGNGame()
print pgn.dumps(pgn.loads(pgn_text)[0])