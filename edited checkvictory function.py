def checkForVictory(pos):
	numinarowp1=0
	numinarowp2=0
	numinarowp3=0
	numinarowp4=0
	for b in range(7):
		for a in range(7): #check vertical and horizontal for win
			if grid[b][a]==1: #checks each collumbs for p1 piece
				numinarowp1+=1
			else:
				numinarowp1=0
			if grid[b][a]==2: #checks for p2 piece
				numinarowp2+=1
			else:
				numinarowp2=0
			if numinarowp1>=4 or numinarowp2>=4:
				return True
			if grid[a][b]==1: #checks each row for p1 piece
				numinarowp3+=1
			else:
				numinarowp3=0
			if grid[a][b]==2: #checks for p2 piece
				numinarowp4+=1
			else:
				numinarowp4=0
			if numinarowp3>=4 or numinarowp4>=4:
				return True	
			
	for a in range(7):
		for b in range(7):
			if grid[a][b]==1 and grid[a+1][b+1]==1 and grid[a+2][b+2]==1 and grid[a+3][b+3]==1:
				return True
	for a in range(7):
		for b in range(7):
			if grid[a][b]==1 and grid[a+1][b-1]==1 and grid[a+2][b-2]==1 and grid[a+3][b-3]==1:
				return True			
		
