// Array\Array1.h
#ifndef __CArray1__
#define __CArray1__

//#include <afxwin.h>
#include "Container1.h"
//#include <Array\Defs.h>

//---------------------------------------------------------------------------------
/*! One dimension template array, publicly derived from CContainer1
 *  This class offers several processing operators
 *  Array1 is intended to be instanciated only for numerical types.
 *///------------------------------------------------------------------------------
template <class Type> class CArray1 : public CContainer1<Type>
{
public: 

//---------------------------------------------------------------------------------
/*! Constructor : dynamic memory allocation, but not initialized with any value.
 *  @param p_Width size of the array, default value is 0
 *///------------------------------------------------------------------------------
	CArray1(const int p_Width = 0);

//---------------------------------------------------------------------------------
/*! Constructor from an existing memory location. The array elements are 
 *  instantiated with given data
 *  @param p_pSrc pointer on an existing memory location containing data
 *  @param p_Width size of the array
 *///------------------------------------------------------------------------------
  	CArray1(const Type* p_pSrc, const int p_Width);

//---------------------------------------------------------------------------------
/*! Copy Constructor from an existing array.
 *  @param p_pSrc existing array
 *///------------------------------------------------------------------------------
   	CArray1(const CArray1<Type>& p_Src);

//---------------------------------------------------------------------------------
/*! Constructor from an existing array, in the extend of a given size
 *  @param p_pSrc existing array
 *  @param p_Width size of the data to be initialized from the source array
 *///------------------------------------------------------------------------------
	CArray1(const CArray1<Type>& p_Src, const int p_Width);

//---------------------------------------------------------------------------------
/*! Destructor
 *///------------------------------------------------------------------------------
   	virtual ~CArray1(); 



//---------------------------------------------------------------------------------
/*! Add two arrays, element by element. The current array and the parameter array 
 *  are not modified
 *  @param p_Arr array to add to the current array
 *  @return an array : each element is the sum of an element of the current array
 *  and its corresponding element in p_Arr.
 *///------------------------------------------------------------------------------
	CArray1<Type> operator+(const CArray1<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Add the same value to all the elements of the array. The current array is not 
 *  modified.
 *  @param p_Val value to add to all the elements
 *  @return an array : each element is the sum of an element of the current array and
 *  the parameter value.
 *///------------------------------------------------------------------------------
	CArray1<Type> operator+(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Add two arrays, element by element. The current array is modified and contains
 *  the result of the addition.
 *  @param p_Arr the parameter array is added element by element to the current array
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const CArray1<Type>& operator+=(const CArray1<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Add the same value to all the elements of the array. The current array is modified
 *  and contains the result of the addition.
 *  @param p_Val value to add to all the elements
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const CArray1<Type>& operator+=(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Subtract two arrays, element by element. The current array and the parameter array 
 *  are not modified
 *  @param p_Arr array to subtract to the current array
 *  @return an array : each element is the subtraction of an element of the current array
 *  and its corresponding element in p_Arr.
 *///------------------------------------------------------------------------------
	CArray1<Type> operator-(const CArray1<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Subtract the same value to all the elements of the array. The current array is not 
 *  modified.
 *  @param p_Val value to subtract to all the elements
 *  @return an array : each element is the subtraction of an element of the current array and
 *  the parameter value.
 *///------------------------------------------------------------------------------
	CArray1<Type> operator-(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Subtract two arrays, element by element. The current array is modified and contains
 *  the result of the subtraction.
 *  @param p_Arr the parameter array is subtracted element by element from the current array
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const CArray1<Type>& operator-=(const CArray1<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Subtract the same value to all the elements of the array. The current array is modified
 *  and contains the result of the subtraction.
 *  @param p_Val value to subtract to all the elements
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const CArray1<Type>& operator-=(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Multiply two arrays, element by element. The current array and the parameter array 
 *  are not modified
 *  @param p_Arr array to multiply to the current array
 *  @return an array : each element is the multiplication of an element of the current array
 *  by its corresponding element in p_Arr.
 *///------------------------------------------------------------------------------
	CArray1<Type> operator*(const CArray1<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Multiply by the same value all the elements of the array. The current array is not 
 *  modified.
 *  @param p_Val value to multiply to all the elements
 *  @return an array : each element is the multiplication of an element of the current array by
 *  the parameter value.
 *///------------------------------------------------------------------------------
	CArray1<Type> operator*(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Multiply two arrays, element by element. The current array is modified and contains
 *  the result of the multiplication.
 *  @param p_Arr the parameter array is multiplied element by element by the current array
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const CArray1<Type>& operator*=(const CArray1<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Multiply by the same value all the elements of the array. The current array is modified
 *  and contains the result of the multiplication.
 *  @param p_Val value by which to multiply to all the elements
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const CArray1<Type>& operator*=(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Subdivide two arrays, element by element. The current array and the parameter array 
 *  are not modified.
 *  @param p_Arr array to subdivide to the current array
 *  @return an array : each element is the subdivision of an element of the current array
 *  by its corresponding element in p_Arr.
 *///------------------------------------------------------------------------------
	CArray1<Type> operator/(const CArray1<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Subdivide by the same value all the elements of the array. The current array is not 
 *  modified.
 *  @param p_Val value to subdivide to all the elements
 *  @return an array : each element is the subdivision of an element of the current array by
 *  the parameter value.
 *///------------------------------------------------------------------------------
	CArray1<Type> 	operator/(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Subdivide two arrays, element by element. The current array is modified and contains
 *  the result of the subdivision.
 *  @param p_Arr the parameter array is subdivided element by element by the current array
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const	CArray1<Type>& 	operator/=(const CArray1<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Subdivide by the same value all the elements of the array. The current array is modified
 *  and contains the result of the subdivision.
 *  @param p_Val value by which to subdivide to all the elements
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const	CArray1<Type>& 	operator/=(const Type p_Val);

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
	void	Convert(CArray1<char>& p_Result) const;
	void	Convert(CArray1<char>& p_Result) const;
	void	Convert(CArray1<short>& p_Result) const;
	//void	Convert(CArray1<WORD>& p_Result) const;
	void	Convert(CArray1<int>& p_Result) const;
	//void	Convert(CArray1<UINT>& p_Result) const;
	void	Convert(CArray1<long>& p_Result) const;
	//void	Convert(CArray1<DWORD>& p_Result) const;
	void	Convert(CArray1<float>& p_Result) const;
	void	Convert(CArray1<double>& p_Result) const;


//---------------------------------------------------------------------------------
/*! Find minimum value in the array
 *  @param p_NoZero boolean : if true, 0 is excluded from search, 
 *  else 0 is taken into account, default value is false. 
 *  @return minimum value in the array
 *///------------------------------------------------------------------------------
   	Type	GetMin(const bool p_NoZero = false) const;

//---------------------------------------------------------------------------------
/*! Find the minimum value and its index in the array. 
 *  @param p_Pos will contain the index of the minimum value in the array
 *  @return minimum value in the array
 *///------------------------------------------------------------------------------
   	Type	GetMinPos(int& p_Pos) const;

//---------------------------------------------------------------------------------
/*! Find maximum value in the array
 *  @param p_NoZero boolean : if true, 0 is excluded from search, 
 *  else 0 is taken into account, default value is false. 
 *  @return maximum value in the array
 *///------------------------------------------------------------------------------
  	Type	GetMax(const bool noZero = false) const;

//---------------------------------------------------------------------------------
/*! Find the maximum value and its index in the array. 
 *  @param p_Pos will contain the index of the maximum value in the array
 *  @return maximum value in the array
 *///------------------------------------------------------------------------------
   	Type	GetMaxPos(int& pos) const;

//---------------------------------------------------------------------------------
/*! Compute the mean value of the array
 *  @image html Array1_GetMean.bmp
 *  @return mean value, converted to 'double' type.
 *///------------------------------------------------------------------------------
	double	GetMean() const;

//---------------------------------------------------------------------------------
/*! Compute the sum of all the elements in the array
 *  @image html Array1_GetSum.bmp
 *  @return sum, converted to 'double' type.
 *///------------------------------------------------------------------------------
  	double	GetSum() const;

//---------------------------------------------------------------------------------
/*! Compute the energy of all the elements in the array
 *  @image html Array1_GetEnergy.bmp
 *  @return energy, converted to 'double' type.
 *///------------------------------------------------------------------------------
	double	GetEnergy() const;																				

//---------------------------------------------------------------------------------
/*! Compute the entropy of all the elements in the array
 *  @image html Array1_GetEntropy.bmp
 *  @return entropy, converted to 'double' type.
 *///------------------------------------------------------------------------------
	double	GetEntropy() const;						
	
//---------------------------------------------------------------------------------
/*! Compute the homogeneity of all the elements in the array 
 *  @image html Array1_GetHomogeneity.bmp
 *  @return homogeneity, converted to 'double' type.
 *///------------------------------------------------------------------------------
	double	GetHomogeneity() const;																			

//---------------------------------------------------------------------------------
/*! Compute the inertia of all the elements in the array 
 *  @image html Array1_GetInertia.bmp
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
/*! Simple Mask operation : each element of the array is compared to 0 to create a binary mask.
 *  If the value is different from 0, the corresponding element of the mask will be set to 1,
 *  else it keeps the value 0. The current array is not modified by this binarization.
 *  @param p_Mask array which will contain the result of the binarization, of type 'char'
 *  has to be sized at the same dimension of the current array.
 *///------------------------------------------------------------------------------
	void	GetMask(CArray1<char>& p_Mask) const; 

//---------------------------------------------------------------------------------
/*! Threshold and Simple Mask operations are applied to the current array to create a binary mask.
 *  The current array is not modified by the operations.
 *  @param p_Mask array which will contain the result of the binarization, of type 'char'
 *  has to be sized at the same dimension of the current array.
 *  @param p_Threshold threshold value
 *  @param p_Mode comparison mode, default mode is LT
 *///------------------------------------------------------------------------------
	void	GetMask(CArray1<char>& p_Mask, const Type p_Threshold, const ThreshModeEnum p_Mode = LT) const;

//---------------------------------------------------------------------------------
/*! Threshold and Simple Mask operations are applied to the current array to create a binary mask.
 *  The current array is not modified by the operations.
 *  @param p_Mask array which will contain the result of the binarization, of type 'char'
 *  has to be sized at the same dimension of the current array.
 *  @param p_ZeroToOneThershold value in the interval [0.0 .. 1.0], representing a 
 *  percentage of the Maximum value. The actual threshold value will be p_ZeroToOneThershold * Maximum
 *  @param p_Mode comparison mode, default mode is LT.
 *///------------------------------------------------------------------------------
	void	GetMask(CArray1<char>& p_Mask, const long double p_ZeroToOneThershold, const ThreshModeEnum p_Mode = LT) const;

//---------------------------------------------------------------------------------
/*! Double Threshold and Simple Mask operations are applied to the current array to create a binary mask.
 *  The current array is not modified by the operations.
 *  @param p_Mask array which will contain the result of the binarization, of type 'char'
 *  has to be sized at the same dimension of the current array.
 *  @param p_MinThreshold first threshold value for the first comparison
 *  @param p_MaxThreshold second threshold value for the second comparison
 *  @param p_MinMode first comparison mode, default mode is LT
 *  @param p_MaxMode second comparison mode, default mode is GEQ
 *///------------------------------------------------------------------------------
	void	GetMask(CArray1<char>& p_Mask, const Type p_MinThreshold, const Type p_MaxThreshold, 
					const ThreshModeEnum p_MinMode = LT, const ThreshModeEnum p_MaxMode = GEQ) const;

//---------------------------------------------------------------------------------
/*! Binary operation : Apply a binary mask on the current array, using the binary operator OR.
 *  The current array is modified by the application of the mask.
 *  @param p_Mask the binary mask
 *///------------------------------------------------------------------------------
	void	Or(const CArray1<char>& p_Mask);				

//---------------------------------------------------------------------------------
/*! Binary operation : Apply a binary mask on the current array, using the binary operator AND.
 *  The current array is modified by the application of the mask.
 *  @param p_Mask the binary mask
 *///------------------------------------------------------------------------------
	void	And(const CArray1<char>& p_Mask);					

//---------------------------------------------------------------------------------
/*! Binary operation : Apply a binary mask on the current array, using the binary operator XOR.
 *  The current array is modified by the application of the mask.
 *  @param p_Mask the binary mask
 *///------------------------------------------------------------------------------
	void	Xor(const CArray1<char>& p_Mask);					

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
	void	Mask(const CArray1<char>& p_Mask);				

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
 *  @image html Array1_GetCorrelation.bmp
 *  The current array is not modified.
 *  @param p_Arr the second array to compute the correlation with, not modified.
 *  @return the correlation between current array and parameter array, converted to type 'double'.
 *///------------------------------------------------------------------------------
	double	GetCorrelation(CArray1<Type>& p_Arr) const;

//---------------------------------------------------------------------------------
/*! Sorting function. The current array is modified
 *  @param p_bAscending flag to indicate the sorting order : true is ascending order,
 *  false is descending order. Default value is true.
 *///------------------------------------------------------------------------------
	void	Qsort(const bool p_bAscending = true);

};

#endif //__CArray1__
