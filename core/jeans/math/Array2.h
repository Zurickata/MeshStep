// Array\Array2.h
#ifndef __CArray2__
#define __CArray2__

//#include <afxwin.h>
#include "../Array/Container2.h"
#include "../Array/Array1.h"
#include "../Array/Defs.h"

//---------------------------------------------------------------------------------
/*! One dimension template array, publicly derived from CContainer2
 *  This class offers several processing operators
 *  Array2 is intended to be instanciated only for numerical types.
 *///------------------------------------------------------------------------------
template <class Type> class CArray2 : public CContainer2<Type>
{
public: 

//---------------------------------------------------------------------------------
/*! Constructor : dynamic memory allocation, but not initialized with any value.
 *  @param p_Height height of the array, (1rst dimension), default value is 0
 *  @param p_Width width of the array, (2nd dimension), default value is 0
 *///------------------------------------------------------------------------------
	CArray2(const int p_Height = 0, const int p_Width = 0); 

//---------------------------------------------------------------------------------
/*! Constructor : dynamic memory allocation, but not initialized with any value.
 *  @param p_Size 2D size of the array
 *///------------------------------------------------------------------------------
  	CArray2(const CSize& p_Size); 

//---------------------------------------------------------------------------------
/*! Constructor from an existing memory location. The array elements are 
 *  initiated with given data
 *  @param p_pSrc pointer on an existing memory location containing data
 *  @param p_Height height of the array (1rst dimension)
 *  @param p_Width width of the array (2nd dimension)
 *///------------------------------------------------------------------------------
  	CArray2(const Type* p_pSrc, const int p_Height, const int p_Width); 

//---------------------------------------------------------------------------------
/*! Copy Constructor from an existing array.
 *  @param p_Src existing array
 *///------------------------------------------------------------------------------
  	CArray2(const CArray2<Type>& p_Src); 

//---------------------------------------------------------------------------------
/*! Constructor from an existing array, in the extend of a given size
 *  @param p_Src existing array
 *  @param p_Height height of the source array to copy
 *  @param p_Width width of the source array to copy
 *///------------------------------------------------------------------------------
  	CArray2(const CArray2<Type>& p_Src, const int p_Height, const int p_Width); 

//---------------------------------------------------------------------------------
/*! Constructor from an existing array, in the extend of a given size
 *  @param p_Src existing array
 *  @param p_Size 2D size of the source array to copy
 *///------------------------------------------------------------------------------
  	CArray2(const CArray2<Type>& p_Src, const CSize& p_Size); 
//---------------------------------------------------------------------------------
/*! Destructor
 *///------------------------------------------------------------------------------
	virtual ~CArray2(); 

	
//---------------------------------------------------------------------------------
/*! Add two arrays, element by element. The current array and the parameter array 
 *  are not modified
 *  @param p_Arr array to add to the current array
 *  @return an array : each element is the sum of an element of the current array
 *  and its corresponding element in p_Arr.
 *///------------------------------------------------------------------------------
	CArray2<Type> 	operator+(const CArray2<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Add the same value to all the elements of the array. The current array is not 
 *  modified.
 *  @param p_Val value to add to all the elements
 *  @return an array : each element is the sum of an element of the current array and
 *  the parameter value.
 *///------------------------------------------------------------------------------
	CArray2<Type> 	operator+(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Add two arrays, element by element. The current array is modified and contains
 *  the result of the addition.
 *  @param p_Arr the parameter array is added element by element to the current array
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const	CArray2<Type>& 	operator+=(const CArray2<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Add the same value to all the elements of the array. The current array is modified
 *  and contains the result of the addition.
 *  @param p_Val value to add to all the elements
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const	CArray2<Type>& 	operator+=(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Subtract two arrays, element by element. The current array and the parameter array 
 *  are not modified
 *  @param p_Arr array to subtract to the current array
 *  @return an array : each element is the subtraction of an element of the current array
 *  and its corresponding element in p_Arr.
 *///------------------------------------------------------------------------------
	CArray2<Type> operator-(const CArray2<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Subtract the same value to all the elements of the array. The current array is not 
 *  modified.
 *  @param p_Val value to subtract to all the elements
 *  @return an array : each element is the subtraction of an element of the current array and
 *  the parameter value.
 *///------------------------------------------------------------------------------
	CArray2<Type> operator-(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Subtract two arrays, element by element. The current array is modified and contains
 *  the result of the subtraction.
 *  @param p_Arr the parameter array is subtracted element by element from the current array
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const CArray2<Type>& operator-=(const CArray2<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Subtract the same value to all the elements of the array. The current array is modified
 *  and contains the result of the subtraction.
 *  @param p_Val value to subtract to all the elements
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const CArray2<Type>& operator-=(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Multiply two arrays, element by element. The current array and the parameter array 
 *  are not modified
 *  @param p_Arr array to multiply to the current array
 *  @return an array : each element is the multiplication of an element of the current array
 *  by its corresponding element in p_Arr.
 *///------------------------------------------------------------------------------
	CArray2<Type> operator*(const CArray2<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Multiply by the same value all the elements of the array. The current array is not 
 *  modified.
 *  @param p_Val value to multiply to all the elements
 *  @return an array : each element is the multiplication of an element of the current array by
 *  the parameter value.
 *///------------------------------------------------------------------------------
	CArray2<Type> operator*(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Multiply two arrays, element by element. The current array is modified and contains
 *  the result of the multiplication.
 *  @param p_Arr the parameter array is multiplied element by element by the current array
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const CArray2<Type>& operator*=(const CArray2<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Multiply by the same value all the elements of the array. The current array is modified
 *  and contains the result of the multiplication.
 *  @param p_Val value by which to multiply to all the elements
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const CArray2<Type>& operator*=(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Subdivide two arrays, element by element. The current array and the parameter array 
 *  are not modified.
 *  @param p_Arr array to subdivide to the current array
 *  @return an array : each element is the subdivision of an element of the current array
 *  by its corresponding element in p_Arr.
 *///------------------------------------------------------------------------------
	CArray2<Type> operator/(const CArray2<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Subdivide by the same value all the elements of the array. The current array is not 
 *  modified.
 *  @param p_Val value to subdivide to all the elements
 *  @return an array : each element is the subdivision of an element of the current array by
 *  the parameter value.
 *///------------------------------------------------------------------------------
	CArray2<Type> 	operator/(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Subdivide two arrays, element by element. The current array is modified and contains
 *  the result of the subdivision.
 *  @param p_Arr the parameter array is subdivided element by element by the current array
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const	CArray2<Type>& 	operator/=(const CArray2<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Subdivide by the same value all the elements of the array. The current array is modified
 *  and contains the result of the subdivision.
 *  @param p_Val value by which to subdivide to all the elements
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const	CArray2<Type>& 	operator/=(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Absolute value of each element of the array. The current array is modified and
 *  contains the result of the operation.
 *///------------------------------------------------------------------------------
	void	Abs();

//---------------------------------------------------------------------------------
/*! Square root of each element of the array. The current array is modified and
 *  contains the result of the operation.
 *  @param p_IfLessZero is the value to which an element will be set if it is negative,
 *  default value is 0.
 *///------------------------------------------------------------------------------
	void	Sqrt(const Type p_IfLessZero = 0);		
	
//---------------------------------------------------------------------------------
/*! Base 10 logarithm of each element of the array. The current array is modified and
 *  contains the result of the operation.
 *  @param p_IfLessZero is the value to which an element will be set if it is null or 
 *  negative, default value is 0.
 *///------------------------------------------------------------------------------
	void	Log10(const Type p_IfLessOrEqZero = 0);	

//---------------------------------------------------------------------------------
/*! Type conversion : current array elements are converted to the type of the  result array.
 *  The current array is not modified.
 *  @param p_Result array, will contain the result of the conversion.
 *///------------------------------------------------------------------------------
	void	Convert(CArray2<char>& p_Result) const;
	void	Convert(CArray2<BYTE>& p_Result) const;
	void	Convert(CArray2<short>& p_Result) const;
	void	Convert(CArray2<WORD>& p_Result) const;
	void	Convert(CArray2<int>& p_Result) const;
	void	Convert(CArray2<UINT>& p_Result) const;
	void	Convert(CArray2<long>& p_Result) const;
	void	Convert(CArray2<DWORD>& p_Result) const;
	void	Convert(CArray2<float>& p_Result) const;
	void	Convert(CArray2<double>& p_Result) const;

//---------------------------------------------------------------------------------
/*! Find minimum value in the array
 *  @param p_NoZero boolean : if true, 0 is excluded from search, 
 *  else 0 is taken into account, default value is false. 
 *  @return minimum value in the array
 *///------------------------------------------------------------------------------
  	Type	GetMin(const bool p_NoZero = false) const;	

//---------------------------------------------------------------------------------
/*! Find the minimum value and its height and width indices in the array. 
 *  @param p_PosY will contain the height index of the minimum value in the array
 *  @param p_PosX will contain the width index of the minimum value in the array
 *  @return minimum value in the array
 *///------------------------------------------------------------------------------
   	Type	GetMinPos(int& p_PosY, int& p_PosX) const;

//---------------------------------------------------------------------------------
/*! Find the minimum value in a given column in the array. 
 *  @param p_Col the column index
 *  @return minimum value in the column
 *///------------------------------------------------------------------------------
  	Type	GetMinCol(const int p_Col) const;

//---------------------------------------------------------------------------------
/*! Find the minimum value in a given raw in the array. 
 *  @param p_Line the raw index
 *  @return minimum value in the raw
 *///------------------------------------------------------------------------------
  	Type	GetMinLine(const int p_Line) const;

//---------------------------------------------------------------------------------
/*! Find maximum value in the array
 *  @param p_NoZero boolean : if true, 0 is excluded from search, 
 *  else 0 is taken into account, default value is false. 
 *  @return maximum value in the array
 *///------------------------------------------------------------------------------
  	Type	GetMax(const bool p_NoZero = false) const;

//---------------------------------------------------------------------------------
/*! Find the maximum value and its height and width indices in the array. 
 *  @param p_PosY will contain the height index of the maximum value in the array
 *  @param p_PosX will contain the width index of the maximum value in the array
 *  @return maximum value in the array
 *///------------------------------------------------------------------------------
   	Type	GetMaxPos(int& p_PosY, int& p_PosX) const;

//---------------------------------------------------------------------------------
/*! Find the maximum value in a given column in the array. 
 *  @param p_Col the column index
 *  @return maximum value in the column
 *///------------------------------------------------------------------------------
  	Type	GetMaxCol(const int p_Col) const;

//---------------------------------------------------------------------------------
/*! Find the maximum value in a given raw in the array. 
 *  @param p_Line the raw index
 *  @return maximum value in the raw
 *///------------------------------------------------------------------------------
  	Type	GetMaxLine(const int p_Line) const;

//---------------------------------------------------------------------------------
/*! Compute the mean value of the array
 *  @image html Array2_GetMean.bmp
 *  @return mean value, converted to 'double' type.
 *///------------------------------------------------------------------------------
  	double	GetMean() const;

//---------------------------------------------------------------------------------
/*! Compute the sum of all the elements in the array
 *  @image html Array2_GetSum.bmp
 *  @return sum, converted to 'double' type.
 *///------------------------------------------------------------------------------
  	double	GetSum() const;

//---------------------------------------------------------------------------------
/*! Compute the energy of all the elements in the array 
 *  @image html Array2_GetEnergy.bmp
 *  @return energy, converted to 'double' type.
 *///------------------------------------------------------------------------------
	double	GetEnergy() const;																				

//---------------------------------------------------------------------------------
/*! Compute the entropy of all the elements in the array 
 *  @image html Array2_GetEntropy.bmp
 *  @return entropy, converted to 'double' type.
 *///------------------------------------------------------------------------------
	double	GetEntropy() const;						
	
//---------------------------------------------------------------------------------
/*! Compute the homogeneity of all the elements in the array 
 *  @image html Array2_GetHomogeneity.bmp
 *  @return homogeneity, converted to 'double' type.
 *///------------------------------------------------------------------------------
	double	GetHomogeneity() const;																			

//---------------------------------------------------------------------------------
/*! Compute the inertia of all the elements in the array 
 *  @image html Array2_GetInertia.bmp
 *  @return inertia, converted to 'double' type.
 *///------------------------------------------------------------------------------
	double	GetInertia() const;																		
	
//---------------------------------------------------------------------------------
/*! Theshold operation : for each element in the array, if its value compared to the
 *  threshold value satisfies the comparison condition, then it is set to 0,
 *  else the value is kept. The current array is modified by the operation.
 *  @param p_Threshold threshold value
 *  @param p_Mode comparison mode by which each element value is compared to the threshold value
 *  see file 'Defs.h' for definitions of the comparison modes.
 *  default comparison mode is LT.
 *///------------------------------------------------------------------------------
	void	Threshold(const Type p_Threshold, const ThreshModeEnum p_Mode = LT); 

//---------------------------------------------------------------------------------
/*! Threshold operation : for each element in the array, if its value compared to the
 *  threshold value satisfies the comparison condition, then it is set to 0,
 *  else the value is kept. The current array is modified by the operation.
 *  @param p_ZeroToOneThershold value in the interval [0.0 .. 1.0], representing a 
 *  percentage of the Maximum value. The actual threshold value will be p_ZeroToOneThershold * Maximum
 *  @param p_Mode comparison mode, default mode is LT.
 *///------------------------------------------------------------------------------
	void	Threshold(const long double p_ZeroToOneThershold, const ThreshModeEnum p_Mode = LT);

//---------------------------------------------------------------------------------
/*! Double threshold operation : for each element in the array, if its value satisfies
 *  either one of the comparison conditions, then it is set to 0, else the value is kept. 
 *  The current array is modified by the operation.
 *  @param p_MinThreshold first threshold value for the first comparison
 *  @param p_MaxThreshold second threshold value for the second comparison
 *  @param p_MinMode first comparison mode, default mode is LT
 *  @param p_MaxMode second comparison mode, default mode is GEQ
 *///------------------------------------------------------------------------------
	void	Threshold(const Type p_MinThreshold, const Type p_MaxThreshold, 
				const ThreshModeEnum p_MinMode = LT, const ThreshModeEnum p_MaxMode = GEQ);	
	
//---------------------------------------------------------------------------------
/*! Binarization operation : each element of the array is compared to the threshold value
 *  via the comparison mode. If the comparison condition is satisfied, the element is set
 *  set to 1, else it is set to 0. The current array is modified by the binarization.
 *  @param p_Threshold threshold value, default value is 0
 *  @param p_Mode comparison mode, default mode is GT
 *///------------------------------------------------------------------------------
	void	Binarize(const Type p_Threshold = 0, const ThreshModeEnum p_Mode = GT);

//---------------------------------------------------------------------------------
/*! Compute the minimum bounding rectangle limits containing the binary objects
 *  @param p_OffX return the left vertical limit
 *  @param p_TailX return the right vertical limit
 *  @param p_OffY return the upper horizontal limit
 *  @param p_TailY return the lower horizontal limit
 *  @return boolean : True if there are some binary objects, else false
 *///------------------------------------------------------------------------------
	bool	GetBinaryObjectsLimits(int& p_OffX, int& p_TailX, int& p_OffY, int& p_TailY);

	
	//---------------------------------------------------------------------------------
/*! For a binary array, extract and labelize the different 2D objects in the a sub-part
 *  of the array. The array has to be such that the background pixels are set to 0 and 
 *  the pixels representing the objects are set to a positive number. Only 254 objects 
 *  can be extracted. 
 *  The current array is modified : all the pixels belonging to the same object are 
 *  labelized with the same value, going from 2 to 255.
 *  @image html Array2_Labelize.bmp
 *  @param p_ObSize 1D array will be sized to 256. Each index from 2 to 255 will correspond
 *  to the value of an extracted objects and will contain the number of pixels in that object.
 *  @param p_Val is the value which the 2D objects are set to, defautl value is 1.
 *  @param p_OffY, height offset value, default value is 0
 *  @param p_TailY, height tail value, default value is 100000
 *  @param p_OffY, width offset value, default value is 0
 *  @param p_TailY, width tail value, default value is 100000
 *///------------------------------------------------------------------------------
	void	LabelizeConnectedObjects(CArray1<int>& p_ObSize, const Type p_Val = 1,
				int p_OffY = 0, int p_TailY = 100000,
				int p_OffX = 0, int p_TailX = 100000);

//---------------------------------------------------------------------------------
/*! Simple Mask operation : each element of the array is compared to 0 to create a binary mask.
 *  If the value is different from 0, the corresponding element of the mask will be set to 1,
 *  else it keeps the value 0. The current array is not modified by this binarization.
 *  @param p_Mask array which will contain the result of the binarization, of type 'BYTE'
 *  has to be sized at the same dimension of the current array.
 *///------------------------------------------------------------------------------
	void	GetMask(CArray2<BYTE>& p_Mask) const; 

//---------------------------------------------------------------------------------
/*! Threshold and Simple Mask operations are applied to the current array to create a binary mask.
 *  The current array is not modified by the operations.
 *  @param p_Mask array which will contain the result of the binarization, of type 'BYTE'
 *  has to be sized at the same dimension of the current array.
 *  @param p_Threshold threshold value
 *  @param p_Mode comparison mode, default mode is LT
 *///------------------------------------------------------------------------------
	void	GetMask(CArray2<BYTE>& p_Mask, const Type p_Threshold, const ThreshModeEnum mode = LT) const;

//---------------------------------------------------------------------------------
/*! Threshold and Simple Mask operations are applied to the current array to create a binary mask.
 *  The current array is not modified by the operations.
 *  @param p_Mask array which will contain the result of the binarization, of type 'BYTE'
 *  has to be sized at the same dimension of the current array.
 *  @param p_ZeroToOneThershold value in the interval [0.0 .. 1.0], representing a 
 *  percentage of the Maximum value. The actual threshold value will be p_ZeroToOneThershold * Maximum
 *  @param p_Mode comparison mode, default mode is LT.
 *///------------------------------------------------------------------------------
	void	GetMask(CArray2<BYTE>& p_Mask, const long double p_ZzeroToOneThershold, const ThreshModeEnum p_Mode = LT) const;

//---------------------------------------------------------------------------------
/*! Double Threshold and Simple Mask operations are applied to the current array to create a binary mask.
 *  The current array is not modified by the operations.
 *  @param p_Mask array which will contain the result of the binarization, of type 'BYTE'
 *  has to be sized at the same dimension of the current array.
 *  @param p_MinThreshold first threshold value for the first comparison
 *  @param p_MaxThreshold second threshold value for the second comparison
 *  @param p_MinMode first comparison mode, default mode is LT
 *  @param p_MaxMode second comparison mode, default mode is GEQ
 *///------------------------------------------------------------------------------
	void	GetMask(CArray2<BYTE>& p_Mask, const Type p_MinThreshold, const Type p_MaxThreshold, 
					const ThreshModeEnum p_MinMode = LT, const ThreshModeEnum p_MaxMode = GEQ) const;

//---------------------------------------------------------------------------------
/*! Binary operation : Apply a binary mask on the current array, using the binary operator OR.
 *  The current array is modified by the application of the mask.
 *  @param p_Mask the binary mask
 *///------------------------------------------------------------------------------
	void	Or(const CArray2<BYTE>& p_Mask);				

//---------------------------------------------------------------------------------
/*! Binary operation : Apply a binary mask on the current array, using the binary operator AND.
 *  The current array is modified by the application of the mask.
 *  @param p_Mask the binary mask
 *///------------------------------------------------------------------------------
	void	And(const CArray2<BYTE>& p_Mask);					

//---------------------------------------------------------------------------------
/*! Binary operation : Apply a binary mask on the current array, using the binary operator XOR.
 *  The current array is modified by the application of the mask.
 *  @param p_Mask the binary mask
 *///------------------------------------------------------------------------------
	void	Xor(const CArray2<BYTE>& p_Mask);					

//---------------------------------------------------------------------------------
/*! Binary operation : negation of the current array, using the binary operator NOT.
 *  The current array is modified. 
 *///------------------------------------------------------------------------------
	void	Not();											

//---------------------------------------------------------------------------------
/*! Binary operation : Apply a binary mask on the current array : the element value is kept
 *  if the corresponding mask element is 1, else it is set to 0.
 *  The current array is modified by the application of the mask.
 *  @param p_Mask the binary mask
 *///------------------------------------------------------------------------------
	void	Mask(const CArray2<BYTE>& p_Mask);	
	
//---------------------------------------------------------------------------------
/*! Fill all the elements in the circle defined by its center coordinates and its radius with a given value.
 *  @param p_Center coordinates of the circle center
 *  @param p_Radius radius (in pixels) of the circle
 *  @param p_Value value to set all the elements in the circle with, default value is 1
 *///------------------------------------------------------------------------------
	void	FillCircle(const CPoint& p_Center, int p_Radius, Type p_Value = 1);

//---------------------------------------------------------------------------------
/*! Set the value of the margin elements to 0. The current array is modified.
 *  @param p_CleanWidth the size of the margin to clean, default value is 1.
 *///------------------------------------------------------------------------------
	void	CleanMargins(const int p_CleanWidth = 1);

//---------------------------------------------------------------------------------
/*! Normalization of the current array : if the sum of all the elements is not 0,
 *  then each element is divided by that sum. The current array is modified by the operation
 *  @return boolean : true if the sum is not null and the array is normalized, 
 *  else false and the operation was not normalized.
 *///------------------------------------------------------------------------------
	bool	Normalize();

//---------------------------------------------------------------------------------
/*! Compute the histogram of an array into another array. The current array is not modified
 *  @param p_Result array of type 'UINT', will contain the computed histogram.
 *///------------------------------------------------------------------------------
	void	GetHistogram(CArray1<UINT>& p_Result) const;

//---------------------------------------------------------------------------------
/*! Seach for the first histogram index which element contains the maximum value.
 *  @return the index of the first element containing the maximum value
 *///------------------------------------------------------------------------------
	int		GetHistogramMode() const;

//---------------------------------------------------------------------------------
/*! Compute the minimum histogram index.
 *  @param p_bWithoutZero boolean flag to indicate if 0 is taken into account : if true
 *  0 is excluded, else it is included in the search, default value is true.
 *  @return the minimum index in the histogram.
 *///------------------------------------------------------------------------------
	int		GetHistogramMin(const bool p_bWithoutZero = true) const;

//---------------------------------------------------------------------------------
/*! Compute the maximum histogram index.
 *  @return the maximum index in the histogram.
 *///------------------------------------------------------------------------------
	int		GetHistogramMax() const;

//---------------------------------------------------------------------------------
/*! Compute statistical indices from the array. the current array is not modified.
 *  @param p_XMean will contain mean value of the elements
 *  @param p_X2Mean will contain mean square of the elements
 *  @param p_XVariance will contain the variance of the elements
 *  @param p_NoZero boolean flag : true if value 0 should be excluded from the analyze, 
 *  false if it should be included, default value is false.
 *  @return boolean indicating if the statistics could be computed (false if 0 elements)
 *///------------------------------------------------------------------------------
	bool	GetStatistics(double& p_XMean, double& p_X2Mean, double& p_XVariance, const bool p_NoZero = false) const;

//---------------------------------------------------------------------------------
/*! Compute the correation parameter between the current array and another array.
 *  @image html Array2_GetCorrelation.bmp
 *  The current array is not modified.
 *  @param p_Arr the second array to compute the correlation with, not modified.
 *  @return the correlation between current array and parameter array, converted to type 'double'.
 *///------------------------------------------------------------------------------
	double	GetCorrelation(CArray2<Type>& p_Arr) const;

//---------------------------------------------------------------------------------
/*! Sorting function. The current array is modified
 *  @param p_bAscending flag to indicate the sorting order : true is ascending order,
 *  false is descending order. Default value is true.
 *///------------------------------------------------------------------------------
	void	Qsort(const bool p_bAscending = true);

//---------------------------------------------------------------------------------
/*! Shift the elements of the array by the given offsets. The current array is modified
 *  by the shifting.
 *  @param p_OffX width offset 
 *  @param p_OffY height offset
 *///------------------------------------------------------------------------------
	void	Shift(const int p_OffX, const int p_OffY);

//---------------------------------------------------------------------------------
/*! Shift the elements of the array by the given offset point. The current array is modified
 *  by the shifting.
 *  @param p_Off offset point 
 *///------------------------------------------------------------------------------
	void	Shift(const CPoint& p_Off);

//---------------------------------------------------------------------------------
/*! Transpose the elements of the array. The current array is modified.
 *///------------------------------------------------------------------------------
	void	Transpose();

//---------------------------------------------------------------------------------
/*! Flip the elements of the array in the width direction. The current array is modified.
 *///------------------------------------------------------------------------------
	void	ReflexionX();

//---------------------------------------------------------------------------------
/*! Flip the elements of the array in the height direction. The current array is modified.
 *///------------------------------------------------------------------------------
	void	ReflexionY();

//---------------------------------------------------------------------------------
/*! Flip the elements of the array around its center. The current array is modified.
 *///------------------------------------------------------------------------------
	void	ReflexionCenter();

//---------------------------------------------------------------------------------
/*! Modify the connectivity between elements in a binarized array.
 *  If connectivity mode is 4, then for each element set to 1 such that its NE and NW
 *  neighbours are also set to 1, and its N neighbour is set to 0, then set its N neighbours to 1 also.
 *  If connectivity mode is 8, then for each element set to 1 such that its N, NE and NW
 *  neighbours are also set to 1, then set its N neighbours to 0. 
 *  The current array is modified with the new connectivity.
 *  @param p_Connect connectivity mode, default mode is 4
 *///------------------------------------------------------------------------------
	void	SetConnection(const ConnectModeEnum p_Connect = Connect4);

//---------------------------------------------------------------------------------
/*! For a binarized array, binary object borders detection, according to the connectivity mode 
 *  between neighbour elements and the direction of the border search. The current array is modified.
 *  @param p_Connect the type of connection, default mode is 4
 *  @param direction of the search for the objects borders : North will detect only the northern 
 *  borders, South only the southern borders, default is all direction borders.
 *  All directions (Connect8):
 *  @image html Array2_ZeroCrossAllDir.bmp
 *  North (Connect8):
 *  @image html Array2_ZeroCrossNorth.bmp
 *///------------------------------------------------------------------------------
	void	ZeroCross(const ConnectModeEnum p_Connect = Connect4, const DirEnum p_Dir = AllDir);

//---------------------------------------------------------------------------------
/*! Replace the current array with a sub-part of itself, given starting and ending indices.
 *  @param p_X1 starting column index
 *  @param p_Y1 starting raw index
 *  @param p_X2 ending column index
 *  @param p_Y2 ending raw index
 *///------------------------------------------------------------------------------
	void	SetSubArray(const int p_X1, const int p_Y1, const int p_X2, const int p_Y2);

//---------------------------------------------------------------------------------
/*! Replace the current array with a sub-part of itself, given a starting point and a size.
 *  @param p_Offset starting 2D point
 *  @param p_Size size of the sub-array
 *///------------------------------------------------------------------------------
	void	SetSubArray(const CPoint& p_Offset, const CSize& p_Size);

//---------------------------------------------------------------------------------
/*! Replace the current array with a sub-part of itself, given starting and ending points.
 *  @param p_Offset starting 2D point
 *  @param p_Tail ending 2D point
 *///------------------------------------------------------------------------------
	void	SetSubArray(const CPoint& p_Offset, const CPoint& p_Tail);

//---------------------------------------------------------------------------------
/*! Copy a sub-part of the current array into a destination array, given starting and ending indices.
 *  the current array is not modified.
 *  @param p_X1 starting column index
 *  @param p_Y1 starting raw index
 *  @param p_X2 ending column index
 *  @param p_Y2 ending raw index
 *  @param p_Dest destination array.
 *///------------------------------------------------------------------------------
	void	GetSubArray(const int p_X1, const int p_Y1, const int p_X2, const int p_Y2, CArray2<Type>& p_Dest);

//---------------------------------------------------------------------------------
/*! Copy a sub-part of the current array into a destination array, given a starting point and a size.
 *  @param p_Offset starting 2D point
 *  @param p_Size size of the sub-array
 *  @param p_Dest destination array.
 *///------------------------------------------------------------------------------
	void	GetSubArray(const CPoint& p_Offset, const CSize& p_Size, CArray2<Type>& p_Dest);

//---------------------------------------------------------------------------------
/*! Copy a sub-part of the current array into a destination array, given starting and ending points.
 *  @param p_Offset starting 2D point
 *  @param p_Tail ending 2D point
 *  @param p_Dest destination array.
 *///------------------------------------------------------------------------------
	void	GetSubArray(const CPoint& p_Offset, const CPoint& p_Tail, CArray2<Type>& p_Dest);

//---------------------------------------------------------------------------------
/*! For a binarized array, compute the distance map for the objects in the array. For each 
 *  pixel, an evaluation of the shortest distance to the objects is computed. 
 *  Distance is negative outside the object, positive inside the object.
 *  For each pixel, the distance to the object limits is given in the middle of the pixel,
 *  with the scale factor DIST_FACT (distance unit is pixel)
 *  @param p_Dist the array that will contain the distance map
 *///------------------------------------------------------------------------------
	bool	GetDistanceMap(CArray2<short>& p_Dist) const;

//---------------------------------------------------------------------------------
/*! Shift the array indices to fit the numerical recipies use of arrays : 
 *  The numerical recipies array data structures are implemented the same way as 
 *  our CContainers2. Therefore, this shift is pssible and corresponds to the 
 *  implementation of numerical recipies.
 *  @return a pointer on the array where the elements are shifted by -1
 *///------------------------------------------------------------------------------
	Type**	EnableRecipies();

//---------------------------------------------------------------------------------
/*! Shift the array indices back to normal. Has to be used only after a call to EnableRecipies().
 *  @return a pointer on the array where the elements are shifted by +1
 *///------------------------------------------------------------------------------
	Type**	DisableRecipies();

//! Scale factor used to compute a distance map
	static const int DIST_FACT;

};

#endif //__CArray2__
