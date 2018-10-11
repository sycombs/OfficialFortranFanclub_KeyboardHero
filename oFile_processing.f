! Fortran comment?

program DataOutput
  character(len=45) ::  someData! Adding some buffer
  integer :: x
  open (unit = 10, file = "output.txt", status = "old", &
        action = "read", position = "rewind", iostat = x)
  if (x > 0) stop "Error opening file"
  read(10, *)
  print *, someData
  close(10)
end program DataOutput
