// Array\ArrayTools.h
#ifndef __CArrayTools__
#define __CArrayTools__

//#include <afxwin.h>
#include <Array\Defs.h>

//---------------------------------------------------------------------------------
/*! Group of functions wich are not specific to a array class, but rather common
 *  to all the array classes
 *///------------------------------------------------------------------------------
template <class Type> class CArrayTools
{
public: 

//---------------------------------------------------------------------------------
/*! Addition element by element of two memory locations into a third one.
 *  The three locations are supposed to be the same size, no check is made if they are not.
 *  @param p_pDest the destination memory location which will contain the result
 *  @param p_pSrc1 the first source memory location, not modified
 *  @param p_pSrc2 the second source memory location, not modified
 *  @param p_DimData the dimension of the memory locations
 *///------------------------------------------------------------------------------
	static void Add(Type* p_pDest, Type* p_pSrc1, Type* p_pSrc2, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Addition element by element of two memory locations.
 *  The two locations are supposed to be the same size, no check is made if they are not.
 *  @param p_pDest the destination memory location which will contain the result
 *  @param p_pSrc the source memory location, to be added to p_pDest, not modified
 *  @param p_DimData the dimension of the memory locations
 *///------------------------------------------------------------------------------
	static void Add(Type* p_pDest, Type* p_Src, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Addition of the same value to all the element of a memory location.
 *  @param p_pDest the destination memory location which will contain the result
 *  @param p_Val the value, to be added to p_pDest
 *  @param p_DimData the dimension of the memory location
 *///------------------------------------------------------------------------------
	static void Add(Type* p_pDest, const Type p_Val, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Subtraction element by element of two memory locations into a third one.
 *  The three locations are supposed to be the same size, no check is made if they are not.
 *  @param p_pDest the destination memory location which will contain the result
 *  @param p_pSrc1 the first source memory location, not modified
 *  @param p_pSrc2 the second source memory location, not modified
 *  @param p_DimData the dimension of the memory locations
 *///------------------------------------------------------------------------------
	static void Sub(Type* p_pDest, Type* p_pSrc1, Type* p_pSrc2, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Subtraction element by element of two memory locations.
 *  The two locations are supposed to be the same size, no check is made if they are not.
 *  @param p_pDest the destination memory location which will contain the result
 *  @param p_pSrc the source memory location, to be subtracted from p_pDest, not modified
 *  @param p_DimData the dimension of the memory locations
 *///------------------------------------------------------------------------------
	static void Sub(Type* p_pDest, Type* p_pSrc, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Subtraction of the same value from all the element of a memory location.
 *  @param p_pDest the destination memory location which will contain the result
 *  @param p_Val the value, to be subtracted from p_pDest
 *  @param p_DimData the dimension of the memory location
 *///------------------------------------------------------------------------------
	static void Sub(Type* p_pDest, const Type p_Val, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Multiplication element by element of two memory locations into a third one.
 *  The three locations are supposed to be the same size, no check is made if they are not.
 *  @param p_pDest the destination memory location which will contain the result
 *  @param p_pSrc1 the first source memory location, not modified
 *  @param p_pSrc2 the second source memory location, not modified
 *  @param p_DimData the dimension of the memory locations
 *///------------------------------------------------------------------------------
	static void Mult(Type* p_pDest, Type* p_pSrc1, Type* p_pSrc2, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Multiplication element by element of two memory locations.
 *  The two locations are supposed to be the same size, no check is made if they are not.
 *  @param p_pDest the destination memory location which will contain the result
 *  @param p_pSrc the source memory location, to be multiplied with p_pDest, not modified
 *  @param p_DimData the dimension of the memory locations
 *///------------------------------------------------------------------------------
	static void Mult(Type* p_pDest, Type* p_pSrc, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Multiplication by the same value of all the element of a memory location.
 *  @param p_pDest the destination memory location which will contain the result
 *  @param p_Val the value, to be multiplied with p_pDest
 *  @param p_DimData the dimension of the memory location
 *///------------------------------------------------------------------------------
	static void Mult(Type* p_pDest, const Type p_Val, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Division element by element of two memory locations into a third one.
 *  The three locations are supposed to be the same size, no check is made if they are not.
 *  @param p_pDest the destination memory location which will contain the result
 *  @param p_pSrc1 the first source memory location, not modified
 *  @param p_pSrc2 the second source memory location, not modified
 *  @param p_DimData the dimension of the memory locations
 *///------------------------------------------------------------------------------
	static void Div(Type* p_pDest, Type* p_pSrc1, Type* p_pSrc2, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Division element by element of two memory locations.
 *  The two locations are supposed to be the same size, no check is made if they are not.
 *  @param p_pDest the destination memory location which will contain the result
 *  @param p_pSrc the source memory location, to be subdivided from p_pDest, not modified
 *  @param p_DimData the dimension of the memory locations
 *///------------------------------------------------------------------------------
	static void Div(Type* p_pDest, Type* p_pSrc, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Division by the same value of all the element of a memory location.
 *  @param p_pDest the destination memory location which will contain the result
 *  @param p_Val the value, to be subdivided from p_pDest
 *  @param p_DimData the dimension of the memory location
 *///------------------------------------------------------------------------------
	static void Div(Type* p_pDest, const Type p_Val, const int p_DimData);


//---------------------------------------------------------------------------------
/*! Absolute value of all the elements of a memory location
 *  @param p_pDest the memory location, will be modified and will contain the result
 *  @param p_DimData the dimension of the memory location
 *///------------------------------------------------------------------------------
	static void Abs(Type* p_pDest, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Square root of all the elements of a memory location
 *  @param p_pDest the memory location, will be modified and will contain the result
 *  @param p_DimData the dimension of the memory location
 *  @param p_IfLessZero the value to replace the result with if the element is < 0
 *///------------------------------------------------------------------------------
	static void Sqrt(Type* p_pDest, const int p_DimData, const Type p_IfLessZero);

//---------------------------------------------------------------------------------
/*! Base 10 logarithm of all the elements of a memory location
 *  @param p_pDest the memory location, will be modified and will contain the result
 *  @param p_DimData the dimension of the memory location
 *  @param p_IfLessOrEqZero the value to replace the result with if the element is <= 0
 *///------------------------------------------------------------------------------
	static void Log10(Type* p_pDest, const int p_DimData, const Type p_IfLessOrEqZero);

//---------------------------------------------------------------------------------
/*! Find the minimum value in all the elements of a memory location
 *  @param p_pSrc the source memory location, not modified
 *  @param p_DimData the dimension of the memory location
 *  @param p_NoZero flag to exclude or not 0 from the search : if true 0 is excluded
 *  else 0 is taken into account.
 *  @return the minimum value
 *///------------------------------------------------------------------------------
	static Type GetMin(Type* p_pSrc, const int p_DimData, const bool p_NoZero);

//---------------------------------------------------------------------------------
/*! Find the minimum value a sample of the elements of a memory location, by searching
 *  with a given step
 *  @param p_pSrc the source memory location, not modified
 *  @param p_DimData the dimension of the memory location
 *  @param p_NoZero flag to exclude or not 0 from the search : if true 0 is excluded
 *  else 0 is taken into account.
 *  @return the minimum value
 *///------------------------------------------------------------------------------
	static Type GetMin(const int p_Incr, Type* p_pSrc, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Find the minimum value and its position in all the elements of a memory location
 *  @param p_pSrc the source memory location, not modified
 *  @param p_DimData the dimension of the memory location
 *  @param p_Pos will contain the position of the minimum value in the memory location.
 *  @return the minimum value
 *///------------------------------------------------------------------------------
	static Type GetMinPos(Type* p_pSrc, const int p_DimData, int& p_Pos);

//---------------------------------------------------------------------------------
/*! Find the maximum value in all the elements of a memory location
 *  @param p_pSrc the source memory location, not modified
 *  @param p_DimData the dimension of the memory location
 *  @param p_NoZero flag to exclude or not 0 from the search : if true 0 is excluded
 *  else 0 is taken into account.
 *  @return the maximum value
 *///------------------------------------------------------------------------------
	static Type GetMax(Type* p_pSrc, const int p_DimData, const bool p_NoZero);

//---------------------------------------------------------------------------------
/*! Find the maximum value a sample of the elements of a memory location, by searching
 *  with a given step
 *  @param p_pSrc the source memory location, not modified
 *  @param p_DimData the dimension of the memory location
 *  @param p_NoZero flag to exclude or not 0 from the search : if true 0 is excluded
 *  else 0 is taken into account.
 *  @return the maximum value
 *///------------------------------------------------------------------------------
	static Type GetMax(const int p_Incr, Type* p_pSrc, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Find the maximum value and its position in all the elements of a memory location
 *  @param p_pSrc the source memory location, not modified
 *  @param p_DimData the dimension of the memory location
 *  @param p_Pos will contain the position of the maximum value in the memory location.
 *  @return the maximum value
 *///------------------------------------------------------------------------------
	static Type GetMaxPos(Type* p_pSrc, const int p_DimData, int& p_Pos);

//---------------------------------------------------------------------------------
/*! Compute the sum of all the elements in a memory location
 *  @param p_pSrc the source memory location, not modified
 *  @param p_DimData the dimension of the memory location
 *  @return the sum of all the elements, converted to 'double' type.
 *///------------------------------------------------------------------------------
	static double GetSum(Type* p_pSrc, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Compute the energy of all the elements in a memory location
 *  (sum of the squared elements : sum(x[i]*x[i]))
 *  @param p_pSrc the source memory location, not modified
 *  @param p_DimData the dimension of the memory location
 *  @return the energy of all the elements, converted to 'double' type.
 *///------------------------------------------------------------------------------
	static double GetEnergy(Type* p_pSrc, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Compute the entropy of all the elements in a memory location
 *  (sum(-x[i]*log10(x[i])) if x[i] > 0)
 *  @param p_pSrc the source memory location, not modified
 *  @param p_DimData the dimension of the memory location
 *  @return the entropy of all the elements, converted to 'double' type.
 *///------------------------------------------------------------------------------
	static double GetEntropy(Type* p_pSrc, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Compute the homogenieity of all the elements in a memory location
 *  (sum(x[i]/(1 + ii*ii)))
 *  @param p_pSrc the source memory location, not modified
 *  @param p_DimData the dimension of the memory location
 *  @return the homogenieity of all the elements, converted to 'double' type.
 *///------------------------------------------------------------------------------
	static double GetHomogeneity(Type* p_pSrc, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Compute the inertia of all the elements in a memory location
 *  (sum(x[i]*ii*ii))
 *  @param p_pSrc the source memory location, not modified
 *  @param p_DimData the dimension of the memory location
 *  @return the inertia of all the elements, converted to 'double' type.
 *///------------------------------------------------------------------------------
	static double GetInertia(Type* p_pSrc, const int p_DimData);


//---------------------------------------------------------------------------------
/*! Threshold operation : for each element in the memory location, if its value compared to the
 *  threshold value satisfies the comparison condition, then it is set to 0,
 *  else the value is kept. The memory is modified at this location.
 *  @param p_pSrc the source memory location
 *  @param p_DimData the dimension of the memory location
 *  @param p_Threshold threshold value
 *  @param p_Mode comparison mode of each element value to the threshold value
 *  see file 'Defs.h' for definitions of the comparison modes.
 *///------------------------------------------------------------------------------
	static void Threshold(Type* p_pSrc, const int p_DimData, const Type p_Threshold, const ThreshModeEnum p_Mode);

//---------------------------------------------------------------------------------
/*! Binarization operation : each element of the memory location is compared to a threshold value
 *  via a comparison mode. If the comparison condition is satisfied, the element is set
 *  set to 1, else it is set to 0. The memory is modified by the binarization.
 *  @param p_pSrc the source memory location
 *  @param p_DimData the dimension of the memory location
 *  @param p_Threshold threshold value
 *  @param p_Mode comparison mode
 *///------------------------------------------------------------------------------
	static void Binarize(Type* p_pSrc, const int p_DimData, const Type p_Threshold, const ThreshModeEnum p_Mode);

//---------------------------------------------------------------------------------
/*! Direct binarization operation : each element of a memory location is compared to 0.
 *  If it is different then the value at this element is set to 1, else it stays 0.
 *  @param p_pDest destination memory location, of type 'BYTE', it will contain the 
 *  result of the binarization.
 *  @param p_pSrc source memory location, not modified by the binarization
 *  @param p_DimData the dimension of the memory locations. Both memory locations
 *  are supposed the same size, no test is made to check it.
 *///------------------------------------------------------------------------------
	static void GetMask(BYTE* p_pDest, Type* p_pSrc, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Binary operation : application of a binary mask on the elements of a memory location,
 *  using the binary operator OR, if the mask has the same size as the source memory.
 *  @param p_pSrc source memory location, is modified by the application of the mask. 
 *  @param p_pMask mask memory location of type 'BYTE'
 *  @param p_DimData the dimension of the memory locations. 
 *///------------------------------------------------------------------------------
	static void Or(Type* p_pSrc, BYTE* p_pMask, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Binary operation : application of a binary mask on the elements of a memory location,
 *  using the binary operator AND, if the mask has the same size as the source memory.
 *  @param p_pSrc source memory location, is modified by the application of the mask. 
 *  @param p_pMask mask memory location of type 'BYTE'
 *  @param p_DimData the dimension of the memory locations. 
 *///------------------------------------------------------------------------------
	static void And(Type* p_pSrc, BYTE* p_pMask, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Binary operation : application of a binary mask on the elements of a memory location,
 *  using the binary operator XOR, if the mask has the same size as the source memory.
 *  @param p_pSrc source memory location, is modified by the application of the mask. 
 *  @param p_pMask mask memory location of type 'BYTE'
 *  @param p_DimData the dimension of the memory locations. 
 *///------------------------------------------------------------------------------
	static void Xor(Type* p_pSrc, BYTE* p_pMask, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Binary operation : negation of the elements of a memory location,
 *  using the binary operator NOT.
 *  @param p_pSrc source memory location, is modified by the operation. 
 *  @param p_DimData the dimension of the memory location. 
 *///------------------------------------------------------------------------------
	static void Not(Type* p_pSrc, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Binary operation : application of a binary mask on the elements of a memory location,
 *  The value of the element is kept if the corresponding value of the mask is 1, else
 *  it is set to 0, if the mask has the same size as the source memory.
 *  @param p_pSrc source memory location, is modified by the application of the mask. 
 *  @param p_pMask mask memory location of type 'BYTE'
 *  @param p_DimData the dimension of the memory locations. 
 *///------------------------------------------------------------------------------
	static void Mask(Type* p_pSrc, BYTE* p_pMask, const int p_DimData);


//---------------------------------------------------------------------------------
/*! Compute the histogram of the elements in a memory location
 *  @param p_pDest the memory location of type 'UINT' sized to proper dimension,
 *  all elements initialized to 0, which will contain the histogram values.
 *  @param p_pSrc source memory location, is not modified. 
 *  @param p_DimData the dimension of the source memory location. 
 *///------------------------------------------------------------------------------
	static void GetHistogram(UINT* p_pDest, Type* p_pSrc, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Compute statistical indices from the elements of a memory location
 *  @param p_pSrc source memory location to be analyzed, not modified.
 *  @param p_DimData the dimension of the source memory location.
 *  @param p_XMean will contain mean value of the elements
 *  @param p_X2Mean will contain mean square of the elements
 *  @param p_XVariance will contain the variance of the elements
 *  @param p_NoZero boolean flag : true if value 0 should be excluded from the analyze, 
 *  false if it should be included.
 *  @return boolean indicating if the statistics could be computed (false if 0 elements)
 *///------------------------------------------------------------------------------
	static bool GetStatistics(Type* p_pSrc, const int p_DimData,
	double& p_XMean, double& p_X2Mean, double& p_XVariance, const bool p_NoZero);

//---------------------------------------------------------------------------------
/*! Compute the correlation parameter from two memory locations of the same size.
 *  No test is made to check the sizes.
 *  @param p_pSrc1 is the first source memory location, not modified
 *  @param p_pSrc2 is the second source memory location, not modified
 *  @param p_DimData the dimension of the memory locations. 
 *  @return the correlation between the elements of the two memory locations.
 *///------------------------------------------------------------------------------
	static double GetCorrelation(Type* p_pSrc1, Type* p_pSrc2, const int p_DimData);


//---------------------------------------------------------------------------------
/*! Sorting the elements of a memory location
 *  @param p_pSrc source memory location to sort, is modified by the operation
 *  @param p_DimData the dimension of the memory location.
 *  @param p_bAscending flag to indicate the sorting order : true is ascending order,
 *  false is descending order. 
 *///------------------------------------------------------------------------------
	static void Qsort(Type* p_pSrc, const int p_DimData, const bool p_bAscending);

//---------------------------------------------------------------------------------
/*! Sorting in ascending order the elements of a memory location
 *  @param p_pData source memory location to sort, is modified by the operation
 *  @param p_Low starting position for the sorting
 *  @param p_High ending position for the sorting 
 *///------------------------------------------------------------------------------
	static void QsortAscending(Type* p_pData, int p_Low, int p_High);

//---------------------------------------------------------------------------------
/*! Sorting in descending order the elements of a memory location
 *  @param p_pData source memory location to sort, is modified by the operation
 *  @param p_Low starting position for the sorting
 *  @param p_High ending position for the sorting 
 *///------------------------------------------------------------------------------
	static void QsortDescending(Type* p_pData, int p_Low, int p_High);

};

// Type Conversion template function
//---------------------------------------------------------------------------------
/*! Type conversion of all the elements of a memory location into another type
 *  The two locations are supposed to be the same size, no check is made if they are not.
 *  @param p_pDest the destination memory location which will contain the result
 *  @param p_pSrc the source memory location, to be converted into p_pDest
 *  @param p_DimData the dimension of the memory locations
 *///------------------------------------------------------------------------------
template <class TypeD, class TypeS> void Convert(TypeD* p_pDest, TypeS* p_pSrc, const int p_DimData);




#endif //__CArrayTools__
