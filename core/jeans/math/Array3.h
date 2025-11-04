// Array\Array3.h
#ifndef __CArray3__
#define __CArray3__

//#include <afxwin.h>
#include "Container3.h"
#include "Array1.h"
#include "Array2.h"
#include "Defs.h"
#include "../Geom/Point3D.h"
#include "../Geom/Vector3D.h"

//---------------------------------------------------------------------------------
/*! One dimension template array, publicly derived from CContainer3
 *  This class offers several processing operators
 *  Array3 is intended to be instanciated only for numerical types.
 *///------------------------------------------------------------------------------
template <class Type> class CArray3 : public CContainer3<Type>
{
public: 

//---------------------------------------------------------------------------------
/*! Constructor : dynamic memory allocation, but not initialized with any value.
 *  @param p_Depth depth of the container (1rst dimension), default value is 0
 *  @param p_Height height of the container (2nd dimension), default value is 0
 *  @param p_Width width of the container (3rd dimension), default value is 0
 *///------------------------------------------------------------------------------
  	CArray3(const int p_Depth = 0, const int p_Height = 0, const int p_Width = 0);

//---------------------------------------------------------------------------------
/*! Constructor from an existing memory location. The container elements are 
 *  initiated with given data
 *  @param p_pSrc pointer on an existing memory location containing data
 *  @param p_Depth depth of the container (1srt dimension), default value is 0
 *  @param p_Height height of the container (2nd dimension), default value is 0
 *  @param p_Width width of the container (3rd dimension), default value is 0
 *///------------------------------------------------------------------------------
  	CArray3(const Type* p_pSrc, const int p_Depth, const int p_Height, const int p_Width);

//---------------------------------------------------------------------------------
/*! Copy Constructor from an existing container.
 *  @param p_Src existing container
 *///------------------------------------------------------------------------------
  	CArray3(const CArray3<Type>& p_Src); 

//---------------------------------------------------------------------------------
/*! Destructor
 *///------------------------------------------------------------------------------
	virtual ~CArray3(); 

	
//---------------------------------------------------------------------------------
/*! Add two arrays, element by element. The current array and the parameter array 
 *  are not modified
 *  @param p_Arr array to add to the current array
 *  @return an array : each element is the sum of an element of the current array
 *  and its corresponding element in p_Arr.
 *///------------------------------------------------------------------------------
	CArray3<Type> 	operator+(const CArray3<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Add the same value to all the elements of the array. The current array is not 
 *  modified.
 *  @param p_Val value to add to all the elements
 *  @return an array : each element is the sum of an element of the current array and
 *  the parameter value.
 *///------------------------------------------------------------------------------
	CArray3<Type> 	operator+(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Add two arrays, element by element. The current array is modified and contains
 *  the result of the addition.
 *  @param p_Arr the parameter array is added element by element to the current array
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const	CArray3<Type>& 	operator+=(const CArray3<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Add the same value to all the elements of the array. The current array is modified
 *  and contains the result of the addition.
 *  @param p_Val value to add to all the elements
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const	CArray3<Type>& 	operator+=(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Subtract two arrays, element by element. The current array and the parameter array 
 *  are not modified
 *  @param p_Arr array to subtract to the current array
 *  @return an array : each element is the subtraction of an element of the current array
 *  and its corresponding element in p_Arr.
 *///------------------------------------------------------------------------------
	CArray3<Type> operator-(const CArray3<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Subtract the same value to all the elements of the array. The current array is not 
 *  modified.
 *  @param p_Val value to subtract to all the elements
 *  @return an array : each element is the subtraction of an element of the current array and
 *  the parameter value.
 *///------------------------------------------------------------------------------
	CArray3<Type> operator-(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Subtract two arrays, element by element. The current array is modified and contains
 *  the result of the subtraction.
 *  @param p_Arr the parameter array is subtracted element by element from the current array
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const CArray3<Type>& operator-=(const CArray3<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Subtract the same value to all the elements of the array. The current array is modified
 *  and contains the result of the subtraction.
 *  @param p_Val value to subtract to all the elements
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const CArray3<Type>& operator-=(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Multiply two arrays, element by element. The current array and the parameter array 
 *  are not modified
 *  @param p_Arr array to multiply to the current array
 *  @return an array : each element is the multiplication of an element of the current array
 *  by its corresponding element in p_Arr.
 *///------------------------------------------------------------------------------
	CArray3<Type> operator*(const CArray3<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Multiply by the same value all the elements of the array. The current array is not 
 *  modified.
 *  @param p_Val value to multiply to all the elements
 *  @return an array : each element is the multiplication of an element of the current array by
 *  the parameter value.
 *///------------------------------------------------------------------------------
	CArray3<Type> operator*(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Multiply two arrays, element by element. The current array is modified and contains
 *  the result of the multiplication.
 *  @param p_Arr the parameter array is multiplied element by element by the current array
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const CArray3<Type>& operator*=(const CArray3<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Multiply by the same value all the elements of the array. The current array is modified
 *  and contains the result of the multiplication.
 *  @param p_Val value by which to multiply to all the elements
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const CArray3<Type>& operator*=(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Subdivide two arrays, element by element. The current array and the parameter array 
 *  are not modified.
 *  @param p_Arr array to subdivide to the current array
 *  @return an array : each element is the subdivision of an element of the current array
 *  by its corresponding element in p_Arr.
 *///------------------------------------------------------------------------------
	CArray3<Type> operator/(const CArray3<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Subdivide by the same value all the elements of the array. The current array is not 
 *  modified.
 *  @param p_Val value to subdivide to all the elements
 *  @return an array : each element is the subdivision of an element of the current array by
 *  the parameter value.
 *///------------------------------------------------------------------------------
	CArray3<Type> 	operator/(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Subdivide two arrays, element by element. The current array is modified and contains
 *  the result of the subdivision.
 *  @param p_Arr the parameter array is subdivided element by element by the current array
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const	CArray3<Type>& 	operator/=(const CArray3<Type>& p_Arr);

//---------------------------------------------------------------------------------
/*! Subdivide by the same value all the elements of the array. The current array is modified
 *  and contains the result of the subdivision.
 *  @param p_Val value by which to subdivide to all the elements
 *  @return a reference to the modified current array
 *///------------------------------------------------------------------------------
	const	CArray3<Type>& 	operator/=(const Type p_Val);

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
	void	Convert(CArray3<char>& p_Result) const;
	void	Convert(CArray3<BYTE>& p_Result) const;
	void	Convert(CArray3<short>& p_Result) const;
	void	Convert(CArray3<WORD>& p_Result) const;
	void	Convert(CArray3<int>& p_Result) const;
	void	Convert(CArray3<UINT>& p_Result) const;
	void	Convert(CArray3<long>& p_Result) const;
	void	Convert(CArray3<DWORD>& p_Result) const;
	void	Convert(CArray3<float>& p_Result) const;
	void	Convert(CArray3<double>& p_Result) const;

//---------------------------------------------------------------------------------
/*! Find minimum value in the array
 *  @param p_NoZero boolean : if true, 0 is excluded from search, 
 *  else 0 is taken into account, default value is false. 
 *  @return minimum value in the array
 *///------------------------------------------------------------------------------
  	Type	GetMin(const bool p_NoZero = false) const;	

//---------------------------------------------------------------------------------
/*! Find the minimum value and its depth, height and width indices in the array. 
 *  @param p_PosZ will contain the depth index of the minimum value in the array
 *  @param p_PosY will contain the height index of the minimum value in the array
 *  @param p_PosX will contain the width index of the minimum value in the array
 *  @return minimum value in the array
 *///------------------------------------------------------------------------------
   	Type	GetMinPos(int& p_PosZ, int& p_PosY, int& p_PosX) const;

//---------------------------------------------------------------------------------
/*! Find maximum value in the array
 *  @param p_NoZero boolean : if true, 0 is excluded from search, 
 *  else 0 is taken into account, default value is false. 
 *  @return maximum value in the array
 *///------------------------------------------------------------------------------
  	Type	GetMax(const bool p_NoZero = false) const;

//---------------------------------------------------------------------------------
/*! Find the maximum value and its depth, height and width indices in the array. 
 *  @param p_PosZ will contain the depth index of the maximum value in the array
 *  @param p_PosY will contain the height index of the maximum value in the array
 *  @param p_PosX will contain the width index of the maximum value in the array
 *  @return maximum value in the array
 *///------------------------------------------------------------------------------
   	Type	GetMaxPos(int& p_PosZ, int& p_PosY, int& p_PosX) const;

//---------------------------------------------------------------------------------
/*! Compute the mean value of the array
 *  @image html Array3_GetMean.bmp
 *  @return mean value, converted to 'double' type.
 *///------------------------------------------------------------------------------
  	double	GetMean() const;

//---------------------------------------------------------------------------------
/*! Compute the sum of all the elements in the array
 *  @image html Array3_GetSum.bmp
 *  @return sum, converted to 'double' type.
 *///------------------------------------------------------------------------------
  	double	GetSum() const;

//---------------------------------------------------------------------------------
/*! Compute the energy of all the elements in the array 
 *  @image html Array3_GetEnergy.bmp
 *  @return energy, converted to 'double' type.
 *///------------------------------------------------------------------------------
	double	GetEnergy() const;																				

//---------------------------------------------------------------------------------
/*! Compute the entropy of all the elements in the array 
 *  @image html Array3_GetEntropy.bmp
 *  @return entropy, converted to 'double' type.
 *///------------------------------------------------------------------------------
	double	GetEntropy() const;						
	
//---------------------------------------------------------------------------------
/*! Compute the homogeneity of all the elements in the array 
 *  @image html Array3_GetHomogeneity.bmp
 *  @return homogeneity, converted to 'double' type.
 *///------------------------------------------------------------------------------
	double	GetHomogeneity() const;																			

//---------------------------------------------------------------------------------
/*! Compute the inertia of all the elements in the array 
 *  @image html Array3_GetInertia.bmp
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
/*! Compute the minimum bounding box limits containing the binary objects
 *  @param p_OffX return the left "width" limit
 *  @param p_TailX return the right "width" limit
 *  @param p_OffY return the upper "height" limit
 *  @param p_TailY return the lower "height" limit
 *  @param p_OffZ return the front "depth" limit
 *  @param p_TailZ return the back "depth" limit
 *  @return boolean : True if there are some binary objects, else false
 *///------------------------------------------------------------------------------
	bool	GetBinaryObjectsLimits(int& p_OffX, int& p_TailX, int& p_OffY, int& p_TailY, int& p_OffZ, int& p_TailZ);

//---------------------------------------------------------------------------------
/*! Simple Mask operation : each element of the array is compared to 0 to create a binary mask.
 *  If the value is different from 0, the corresponding element of the mask will be set to 1,
 *  else it keeps the value 0. The current array is not modified by this binarization.
 *  @param p_Mask array which will contain the result of the binarization, of type 'BYTE'
 *  has to be sized at the same dimension of the current array.
 *///------------------------------------------------------------------------------
	void	GetMask(CArray3<BYTE>& p_Mask) const; 

//---------------------------------------------------------------------------------
/*! Threshold and Simple Mask operations are applied to the current array to create a binary mask.
 *  The current array is not modified by the operations.
 *  @param p_Mask array which will contain the result of the binarization, of type 'BYTE'
 *  has to be sized at the same dimension of the current array.
 *  @param p_Threshold threshold value
 *  @param p_Mode comparison mode, default mode is LT
 *///------------------------------------------------------------------------------
	void	GetMask(CArray3<BYTE>& p_Mask, const Type p_Threshold, const ThreshModeEnum mode = LT) const;

//---------------------------------------------------------------------------------
/*! Threshold and Simple Mask operations are applied to the current array to create a binary mask.
 *  The current array is not modified by the operations.
 *  @param p_Mask array which will contain the result of the binarization, of type 'BYTE'
 *  has to be sized at the same dimension of the current array.
 *  @param p_ZeroToOneThershold value in the interval [0.0 .. 1.0], representing a 
 *  percentage of the Maximum value. The actual threshold value will be p_ZeroToOneThershold * Maximum
 *  @param p_Mode comparison mode, default mode is LT.
 *///------------------------------------------------------------------------------
	void	GetMask(CArray3<BYTE>& p_Mask, const long double p_ZzeroToOneThershold, const ThreshModeEnum p_Mode = LT) const;

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
	void	GetMask(CArray3<BYTE>& p_Mask, const Type p_MinThreshold, const Type p_MaxThreshold, 
					const ThreshModeEnum p_MinMode = LT, const ThreshModeEnum p_MaxMode = GEQ) const;

//---------------------------------------------------------------------------------
/*! Binary operation : Apply a binary mask on the current array, using the binary operator OR.
 *  The current array is modified by the application of the mask.
 *  @param p_Mask the binary mask
 *///------------------------------------------------------------------------------
	void	Or(const CArray3<BYTE>& p_Mask);				

//---------------------------------------------------------------------------------
/*! Binary operation : Apply a binary mask on the current array, using the binary operator AND.
 *  The current array is modified by the application of the mask.
 *  @param p_Mask the binary mask
 *///------------------------------------------------------------------------------
	void	And(const CArray3<BYTE>& p_Mask);					

//---------------------------------------------------------------------------------
/*! Binary operation : Apply a binary mask on the current array, using the binary operator XOR.
 *  The current array is modified by the application of the mask.
 *  @param p_Mask the binary mask
 *///------------------------------------------------------------------------------
	void	Xor(const CArray3<BYTE>& p_Mask);					

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
	void	Mask(const CArray3<BYTE>& p_Mask);				

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
 *  @param p_X3Mean will contain mean square of the elements
 *  @param p_XVariance will contain the variance of the elements
 *  @param p_NoZero boolean flag : true if value 0 should be excluded from the analyze, 
 *  false if it should be included, default value is false.
 *  @return boolean indicating if the statistics could be computed (false if 0 elements)
 *///------------------------------------------------------------------------------
	bool	GetStatistics(double& p_XMean, double& p_X3Mean, double& p_XVariance, const bool p_NoZero = false) const;

//---------------------------------------------------------------------------------
/*! Compute the correation parameter between the current array and another array.
 *  The current array is not modified.
 *  @param p_Arr the second array to compute the correlation with, not modified.
 *  @return the correlation between current array and parameter array, converted to type 'double'.
 *///------------------------------------------------------------------------------
	double	GetCorrelation(CArray3<Type>& p_Arr) const;

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
 *  @param p_OffZ depth offset
 *///------------------------------------------------------------------------------
	void	Shift(const int p_OffX, const int p_OffY, const int p_OffZ);

//---------------------------------------------------------------------------------
/*! Flip the elements of the array in the width direction. The current array is modified.
 *///------------------------------------------------------------------------------
	void	ReflexionX();

//---------------------------------------------------------------------------------
/*! Flip the elements of the array in the height direction. The current array is modified.
 *///------------------------------------------------------------------------------
	void	ReflexionY();

//---------------------------------------------------------------------------------
/*! Flip the elements of the array in the depth direction. The current array is modified.
 *///------------------------------------------------------------------------------
	void	ReflexionZ();

//---------------------------------------------------------------------------------
/*! Flip the elements of the array around its center. The current array is modified.
 *///------------------------------------------------------------------------------
	void	ReflexionCenter();

//---------------------------------------------------------------------------------
/*! Create an isotropic volume : The volume is composed of a set of 2D arrays, isotropic
 *  for the width and height directions. The current 3D array is not modified.
 *  @param p_Result resulting isotropic 3D array.
 *  @param p_DimPixX the dimension of a square 2D pixel
 *  @param p_DimPixZ the current depth dimension (space between slices)
 *///------------------------------------------------------------------------------
	void	GetIsotropic(CArray3<Type>& p_Result, const double p_DimPixX, const double p_DimPixZ);

//---------------------------------------------------------------------------------
/*! Create an isotropic volume : The volume is composed of a set of 2D arrays, isotropic
 *  for the width and height directions. The current 3D array is modified to become isoctropic
 *  for the 3 directions.
 *  @param p_DimPixX the dimension of a square 2D pixel
 *  @param p_DimPixZ the current depth dimension (space between slices)
 *///------------------------------------------------------------------------------
	void	SetIsotropic(const double p_DimPixX, const double p_DimPixZ);

//---------------------------------------------------------------------------------
/*! Reslice a volume to get a slice orthogonal to the X direction. The current 3D array is not modified.
 *  @param p_Result 2D array will contain the slice. The array has to be sized to the size you expect.
 *  @param p_PosX width coordinate in the volume where the slice will be cut.
 *  @param p_PosY height coordinate in the volume where the slice will be cut.
 *  @param p_PosZ depth coordinate in the volume where the slice will be cut.
 *  @param p_ZoomFact zoom factor to apply to the slice
 *  @image html Array3_GetSliceX.bmp
 *///------------------------------------------------------------------------------
	void	GetSliceX(CArray2<Type>& p_Result, const int p_PosX, const int p_PosY, const int p_PosZ, const int p_ZoomFact) const;

//---------------------------------------------------------------------------------
/*! Reslice a volume to get a slice orthogonal to the Y direction. The current 3D array is not modified.
 *  @param p_Result 2D array will contain the slice. The array has to be sized to the size you expect.
 *  @param p_PosX width coordinate in the volume where the slice will be cut.
 *  @param p_PosY height coordinate in the volume where the slice will be cut.
 *  @param p_PosZ depth coordinate in the volume where the slice will be cut.
 *  @param p_ZoomFact zoom factor to apply to the slice
 *  @image html Array3_GetSliceY.bmp
 *///------------------------------------------------------------------------------
	void	GetSliceY(CArray2<Type>& p_Result, const int p_PosX, const int p_PosY, const int p_PosZ, const int p_ZoomFact) const;

//---------------------------------------------------------------------------------
/*! Reslice a volume to get a slice orthogonal to the Z direction. The current 3D array is not modified.
 *  @param p_Result 2D array will contain the slice. The array has to be sized to the size you expect.
 *  @param p_PosX width coordinate in the volume where the slice will be cut.
 *  @param p_PosY height coordinate in the volume where the slice will be cut.
 *  @param p_PosZ depth coordinate in the volume where the slice will be cut.
 *  @param p_ZoomFact zoom factor to apply to the slice
 *  @image html Array3_GetSliceZ.bmp
 *///------------------------------------------------------------------------------
	void	GetSliceZ(CArray2<Type>& p_Result, const int p_PosX, const int p_PosY, const int p_PosZ, const int p_ZoomFact) const;

//---------------------------------------------------------------------------------
/*! Compression of a 3D isotropic volume. The new volume is smaller than the source volume
 *  by a compression factor. The values computed for the compressed volume are average values
 *  from the source volume. The current volume is not modified.
 *  @param p_Result resulting 3D array.
 *  @param p_ComprFact compression factor (ex : 2 -> the compressed volume will be half the source volume)
 *///------------------------------------------------------------------------------
	void	GetCompress(CArray3<Type>& p_Result, const int p_ComprFact) const;

//---------------------------------------------------------------------------------
/*! As previous GetCompress function : the current array is modified to contain the compressed volume
 *  @param p_ComprFact compression factor.
 *///------------------------------------------------------------------------------
	void	SetCompress(const int p_ComprFact);
	
//---------------------------------------------------------------------------------
/*! For a binarized array, compute the distance map for the objects in the array. For each 
 *  voxel, an evaluation of the shortest distance to the objects is computed. 
 *  Distance is negative outside the object, positive inside the object.
 *  For each voxel, the distance to the object limits is given in the middle of the voxel,
 *  with the scale factor DIST_FACT (distance unit is voxel)
 *  @param p_Dist the array that will contain the distance map
 *  @param p_bCityBlock flag to indicat if CityBlock pattern is used to compute the distance map.
 *  default value is false.
 *///------------------------------------------------------------------------------
	bool	GetDistanceMap(CArray3<short>& p_Dist, const bool p_bCityBlock = false) const;

//---------------------------------------------------------------------------------
/*! Calcul générique d'une coupe oblique dans le volume
 *  @param p_Result Image résultat, doit être dimensionnée à la taille souhaitée
 *  @param p_Center point dans le volume autour duquel l'image sera centrée (en voxels)
 *  @param p_VectX vecteur donnant la direction X de l'image a calculer (en voxels)
 *  @param p_VectY vecteur donnant la direction Y de l'image a calculer (en voxels)
 *	@param p_VoxelSizeX dimension du voxel en X
 *	@param p_VoxelSizeY dimension du voxel en Y
 *	@param p_VoxelSizeZ dimension du voxel en Z
 *  @param p_ZoomFact Zoom que l'on souhaite appliquer pour le calcul de l'image
 *  @param p_Size taille de la zone centrale sur laquelle l'image est interpolee
 *///------------------------------------------------------------------------------
	bool	GetObliqueSlice(CArray2<Type>& p_Result, const CPoint3D& p_Center, 
			CVector3D &p_VectX, CVector3D &p_VectY, 
			double p_VoxelSizeX , double p_VoxelSizeY , double p_VoxelSizeZ,
			double p_ZoomFact = 1.0, CSize p_Size = CSize(0,0));

//! Scale factor used to compute a distance map
	static const int DIST_FACT;


protected:

//---------------------------------------------------------------------------------
/*! Transforme un point du volume donné en Voxel (coord entières) en MM.
 *  @param p_VoxelCoord le point en voxel
 *	@param p_DimVoxelX dimension d'un voxel en X
 *	@param p_DimVoxelY dimension d'un voxel en Y
 *	@param p_DimVoxelZ dimension d'un voxel en Z
 *  @param p_MMCoord paramètre retour: le point en mm
 *///------------------------------------------------------------------------------
	inline void VoxelToMM(const CPoint3D& p_VoxelCoord, double p_DimVoxelX, 
		double p_DimVoxelY, double p_DimVoxelZ, CPoint3D& p_MMCoord);
	
//---------------------------------------------------------------------------------
/*! Transforme un point du volume donné en MM en Voxel (coord entières).
 *  @param p_MMCoord le point en mm
 *	@param p_DimVoxelX dimension d'un voxel en X
 *	@param p_DimVoxelY dimension d'un voxel en Y
 *	@param p_DimVoxelZ dimension d'un voxel en Z
 *  @param p_VoxelCoord paramètre retour: le point en voxel
 *///------------------------------------------------------------------------------
	inline void MMToVoxel(const CPoint3D& p_MMCoord, double p_DimVoxelX, 
		double p_DimVoxelY, double p_DimVoxelZ, CPoint3D& p_VoxelCoord);

//---------------------------------------------------------------------------------
/*! Initialization of the distance map. Called inside GetDistanceMap function.
 *  @param p_Dist the array containing the distance map
 *///------------------------------------------------------------------------------
	void	DistanceMapInitialize(CArray3<short>& p_Dist) const;

//---------------------------------------------------------------------------------
/*! Finalization of the distance map. Called inside GetDistanceMap function.
 *  @param p_Dist the array containing the distance map
 *///------------------------------------------------------------------------------
	void	DistanceMapCorrection(CArray3<short>& p_Dist) const;

};

template <class Type> void CArray3<Type>::VoxelToMM(const CPoint3D& p_VoxelCoord,
													double p_DimVoxelX, 
													double p_DimVoxelY, 
													double p_DimVoxelZ,
													CPoint3D& p_MMCoord)
{
	p_MMCoord = CPoint3D(p_VoxelCoord.X() * p_DimVoxelX, 
		p_VoxelCoord.Y() * p_DimVoxelY, 
		p_VoxelCoord.Z() * p_DimVoxelZ);
}

template <class Type> void CArray3<Type>::MMToVoxel(const CPoint3D& p_MMCoord, 
													double p_DimVoxelX, 
													double p_DimVoxelY, 
													double p_DimVoxelZ,
													CPoint3D& p_VoxelCoord)
{
	p_VoxelCoord = CPoint3D((int)(p_MMCoord.X()/ p_DimVoxelX), (int)(p_MMCoord.Y()/ p_DimVoxelY), 
						 (int)(p_MMCoord.Z()/ p_DimVoxelZ));
}


#endif //__CArray3__
