// Array\Defs.h
#ifndef __defs__
#define __defs__

//---------------------------------------------------------------------------------
/*! This files defines several types which are used by all the array classes
 *///------------------------------------------------------------------------------

//! Enumeration of several comparison modes used for Thresholding
enum ThreshModeEnum	{ 
	LT,		//!< Less 
	LEQ,	//!< Less or Equal 
	EQ,		//!< Equal 
	GT, 	//!< Greater
	GEQ, 	//!< Greater or Equal
	NEQ 	//!< Not Equal
};

//! Enumeration of directions used to visit the neighbours of an element in 2D arrays
enum DirEnum {
	Center,			//!< the element itself , no direction
	North,			//!< same column index, lower raw index 
	NorthEast,		//!< higher column index, lower raw index
	East,			//!< higher column index column, same raw index
	SouthEast,		//!< higher column index, higher raw index
	South,			//!< same column index, higher raw index
	SouthWest,		//!< lower column index, higher raw index
	West,			//!< lower column index, same raw index
	NorthWest,		//!< lower column index, lower raw index
	AllDir			//!< any direction
};

//! Enumeration of the two connectivity modes between neighbour elements in 2D arrays
enum ConnectModeEnum { 
	Connect4, //!< consider only the 4 neighbour elements in directions North, South, East, West 
	Connect8 //!< consider the 8 neighbour elements in directions N, S, E, W, NE, NW, SE, SW
};


//---------------------------------------------------------------------------------
/*! Macro definition : swapping of elements at two different positions in a memory location
 *///------------------------------------------------------------------------------
#undef	MSWAP
#define	MSWAP(data, lo, hi)	{	Type val = *(data+lo); *(data+lo) = *(data+hi); *(data+hi) = val; }

#endif //__defs__
