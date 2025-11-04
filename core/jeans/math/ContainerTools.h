// Array\ContainerTools.h
#ifndef __CContainerTools__
#define __CContainerTools__

//#include <afxwin.h>

//---------------------------------------------------------------------------------
/*! This class only contains static functions, commom to all the container classes
 *///------------------------------------------------------------------------------
template <class Type> class CContainerTools
{
public: 

//---------------------------------------------------------------------------------
/*! Initialize all the elements of a given memory location with the same value
 *  @param p_pData pointer to the contiguous memory location
 *  @param p_DimData dimension of the memory to initialize
 *  @param p_Val value with which the memory will be set
 *///------------------------------------------------------------------------------
	static void SetValue(Type* p_pData, const int p_DimData, const Type p_Val);

//---------------------------------------------------------------------------------
/*! Search for a given value in a given memory location (direct comparison of memory bytes)
 *  @param p_pData pointer to the contiguous memory location
 *  @param p_DimData dimension of the memory to initialize
 *  @param p_Val value to look for in the memory location
 *  @return boolean : TRUE if the value is found, else return FALSE 
 *///------------------------------------------------------------------------------
	static bool IsFound(Type* p_pData, const int p_DimData, const Type p_Val);

//---------------------------------------------------------------------------------
/*! Swap the bytes order for each element of a given contiguous memory location
 *  the source container is modified.
 *  @param p_pData pointer to beginning of memory location
 *  @param p_DimData size of memory location
 *///------------------------------------------------------------------------------
	static void ReverseBytes(Type* p_pData, int p_DimData);

//---------------------------------------------------------------------------------
/*! Comparison, element by element of two given memory locations
 *  (direct comparison of memory bytes)
 *  no test is made to check that both containers are the same size.
 *  @param p_pData1 pointer to first element of first memory location
 *  @param p_pData2 pointer to first element of second memory location
 *  @param p_DimData number of element to compare
 *  @return boolean : TRUE if all compared elements are equal, else FALSE
 *///------------------------------------------------------------------------------
	static bool Compare(Type* p_pData1, Type* p_pData2, const int p_DimData);

//---------------------------------------------------------------------------------
/*! Copy, element by element of two given memory locations
 *  (operator= of each element is used)
 *  we assumed that destination is enough allocated
 *  @param p_pData1 pointer to destination buffer
 *  @param p_pData2 pointer from location buffer
 *  @param p_DimData number of element to copy
 *///------------------------------------------------------------------------------
	static void Copy(Type* p_pTo, const Type* p_pFrom, const int p_DimData);
};

#include "ContainerTools.cpp"

#endif //__CContainerTools__

