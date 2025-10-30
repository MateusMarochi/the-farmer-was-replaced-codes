def dinosaur_safe_move(direction):
	# Move in the given direction if possible.
	# If movement is blocked, temporarily change hats as a workaround.
	
	if can_move(direction):
		move(direction)
	else:
		change_hat(Hats.Carrot_Hat)
		change_hat(Hats.Dinosaur_Hat)

clear()
change_hat(Hats.Dinosaur_Hat)
n = get_world_size()
while True:
 for x in range(n):
  # decide vertical target for this column
  if x % 2 == 0:
   target_y = n - 1   # even column index: go to the very top
  else:
   target_y = 1       # odd column index: go down but leave row 0 free
 
  # move vertically until we reach target_y
  while get_pos_y() != target_y:
   if target_y > get_pos_y():
	dinosaur_safe_move(North)
   else:
	dinosaur_safe_move(South)
 
  # after finishing the column, move east if there are more columns
  if x < n - 1:
   move(East)
 
 # finished scanning all columns
 # return to origin using the open bottom row y=0
 # first move down to y=0 (if not already there)
 while get_pos_y() != 0:
  dinosaur_safe_move(South)
 
 # then move west back to x=0
 while get_pos_x() != 0:
  dinosaur_safe_move(West)
 
 # now at (0,0)