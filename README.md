## tables
# Description:
a exel like tabel prosessing programm.
it's in the terminal and exportabel to other types

# Implementation:
saving:
```
Headder:
└─ 8 bytes of type
Body:
├─ 2 bytes of length(y)
└─ Row y times:
	├─ 2 bytes y coord
	├─ 2 bytes of length(x)
	└─ Colum x tinmes:
		├─ 2 bytes of x coord
		├─ 1 byte of color
		├─ 1 byte of string length(w)
		└─ w bytes of string
```
