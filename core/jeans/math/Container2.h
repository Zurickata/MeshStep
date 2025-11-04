// Array\Container2.h

#ifndef __CContainer2__
#define __CContainer2__
#include "Size.h"

//#include <afxwin.h>

//---------------------------------------------------------------------------------
/*! Two dimension template container
 *  @image html Container2.bmp
 *
 *	*****************
 *	!!! ATTENTION !!!
 *	*****************
 *	L'opérateur [] utilisé jusqu'à présent pour affecter ou atteindre une valeur
 *	du container n'est pas fiable (les tests d'index hors limites ne sont pas valables)
 *	Utilisez dès à présent l'opérateur () qui permet de gérer les dépassements.
 *///------------------------------------------------------------------------------
template <class Type> class CContainer2
{
public: 

//---------------------------------------------------------------------------------
/*! Constructor: dynamic memory allocation, but not initialized with any value.
 *  @param p_Height height of the container (1srt dimension), default value is 0
 *  @param p_Width width of the container (2nd dimension), default value is 0
 *///------------------------------------------------------------------------------
  	CContainer2(const int p_Height = 0, const int p_Width = 0);

//---------------------------------------------------------------------------------
/*! Constructor : dynamic memory allocation, but not initialized with any value.
 *  @param p_Size 2D size of the container
 *///------------------------------------------------------------------------------
  	CContainer2(const CSize& p_Size);

//---------------------------------------------------------------------------------
/*! Constructor from an existing memory location. The container elements are 
 *  initiated with given data (direct memory copy)
 *  @param p_pSrc pointer on an existing memory location containing data
 *  @param p_Height height of the container (1srt dimension)
 *  @param p_Width width of the container (2nd dimension)
 *///------------------------------------------------------------------------------
  	CContainer2(const Type* p_pSrc, const int p_Height, const int p_Width);

//---------------------------------------------------------------------------------
/*! Copy Constructor from an existing container.(direct memory copy)
 *  @param p_Src existing container
 *///------------------------------------------------------------------------------
  	CContainer2(const CContainer2<Type>& p_Src); 

//---------------------------------------------------------------------------------
/*! Constructor from an existing container, in the extend of a given size
 *  @param p_Src existing container. (direct memory copy)
 *  @param p_Height height of the source container to copy
 *  @param p_Width width of the source container to copy
 *///------------------------------------------------------------------------------
  	CContainer2(const CContainer2<Type>& p_Src, const int p_Height, const int p_Width); 

//---------------------------------------------------------------------------------
/*! Constructor from an existing container, in the extend of a given size
 *  @param p_Src existing container. (direct memory copy)
 *  @param p_Size 2D size of the source container to copy
 *///------------------------------------------------------------------------------
	CContainer2(const CContainer2<Type>& p_Src, const CSize& p_Size); 


//---------------------------------------------------------------------------------
/*! Destructor
 *///------------------------------------------------------------------------------
   	virtual ~CContainer2();

//---------------------------------------------------------------------------------
/*! Free container memory 
 *///------------------------------------------------------------------------------
	void	Free();


//---------------------------------------------------------------------------------
/*! Setting the size of the container (destroy previous memory and reallocate, but not
 *  initialized with any value)
 *  @param p_Height height of the container
 *  @param p_Width width of the container
 *  @return boolean : true if memory was successfully allocated, else false
 *///------------------------------------------------------------------------------
	bool	SetSize(const int p_Height, const int p_Width);

//---------------------------------------------------------------------------------
/*! Setting the size of the container (destroy previous memory and reallocate, but not
 *  initialized with any value)
 *  @param p_Size 2D size of the container
 *  @return boolean : true if memory was successfully allocated, else false
 *///------------------------------------------------------------------------------
	bool	SetSize(const CSize& p_Size); 

//---------------------------------------------------------------------------------
/*! Access to the size of the container
 *  @return the 2D size of the container
 *///------------------------------------------------------------------------------
	CSize	GetSize() const; 

//---------------------------------------------------------------------------------
/*! Access to the 1srt dimension of the container
 *  @return height of the container
 *///------------------------------------------------------------------------------
	const	int& Height() const { return m_Height; }

//---------------------------------------------------------------------------------
/*! Access to the 2nd dimension of the container
 *  @return width of the container
 *///------------------------------------------------------------------------------
	const	int& Width() const { return m_Width; }

//---------------------------------------------------------------------------------
/*! Access to the number of elements 
 *  @return number of elements
 *///------------------------------------------------------------------------------
	int		GetNbElements() const { return m_Width*m_Height; }

//---------------------------------------------------------------------------------
/*! Access to the size of memeory allocated for the container
 *  @return number of bytes allocated
 *///------------------------------------------------------------------------------
	int		Sizeof() const;

//---------------------------------------------------------------------------------
/*! Access to the address of the first element of the container
 *  @return pointer to the first contiguous memory location of the container
 *///------------------------------------------------------------------------------
  	Type*	GetBuffer() const { return *m_pData; }

//---------------------------------------------------------------------------------
/*! Set all the the elements of the container to the same value
 *  @param p_Val value with which the container elements will be set 
 *///------------------------------------------------------------------------------
	void	SetValue(const Type p_Val); 

//---------------------------------------------------------------------------------
/*! Set a part of the container elements to the same value, starting from a given offset, 
 *  with a given size.
 *  @param p_Val value with which the container elements will be set 
 *  @param p_OffX size of the width-offset, where the setting will start 
 *  @param p_DimX number elements to be set in the width direction
 *  @param p_OffY size of the height-offset, where the setting will start 
 *  @param p_DimY number elements to be set in the height direction
 *///------------------------------------------------------------------------------
  	void	SetValue(const Type p_Val, const int p_OffX, const int p_DimX, const int p_OffY, 
				const int p_DimY);

//---------------------------------------------------------------------------------
/*! Setting a part of the container with a part of another source container
 *  @param p_Src the source container
 *  @param p_OffSrcX size of the width offset in the source container
 *  @param p_TailSrcX width index of the last element to be copied from the source container
 *  @param p_OffSrcY size of the height offset in the source container
 *  @param p_TailSrcY height index of the last element to be copied from the source container
 *  @param p_OffDestX size of the width offset in the destination container, default value is 0
 *  @param p_OffDestY size of the height offset in the destination container, default value is 0
 *///------------------------------------------------------------------------------
	void	GetSubArray(const CContainer2& p_Src, const int p_OffSrcX, const int p_TailSrcX, 
				const int p_OffSrcY, const int p_TailSrcY, const int p_OffDestX = 0, 
				const int p_OffDestY = 0);

//---------------------------------------------------------------------------------
/*! Search for a given value in the container (direct comparison of memory bytes)
 *  @param p_Val the value to look for
 *  @return boolean : true if the value is found, else false
 *///------------------------------------------------------------------------------
	bool	IsFound(const Type p_Val) const; 	

//---------------------------------------------------------------------------------
/*! Byte swaping ( for machine compatibility )
 *///------------------------------------------------------------------------------
	void	Swap();	
	

//---------------------------------------------------------------------------------
/*! Test the validity of the container
 *  @return boolean : true if the memory is allocated properly, else false
 *///------------------------------------------------------------------------------
  	bool	operator!() const; 

//---------------------------------------------------------------------------------
/*! Direct access to container elements, read and write.
 *  Beware : this [] operator is intended to be used with a second [] operator : [j][i]
 *  if only one [] operator is applied, there is no garantee that memory will be preserved.
 *  @param p_Ind index of the "raw" to be accessed
 *  @return a reference of the pointer to the begining of the raw
 *  @warning !! Can't test second index exceeding !!
 *  @sa operator()
 *///------------------------------------------------------------------------------
  	Type*&	operator[](const int p_Ind) const; 

//---------------------------------------------------------------------------------
/*! Direct acces to container elements, read and write.
 *  @param p_Height index of the line to be accessed
 *	@param p_Width index of the raw to be accessed
 *  @return a reference to the element at specified location
 *///------------------------------------------------------------------------------
  	Type&	operator()(const int p_Height, const int p_Width) const; 

//---------------------------------------------------------------------------------
/*! Affectation operator between containers (direct memory copy)
 *  @param p_Src source container to initialize current container with
 *///------------------------------------------------------------------------------
	void	operator=(const CContainer2<Type>& p_Src);

//---------------------------------------------------------------------------------
/*! Value affectation operator
 *  @param p_Val value to initialize the container elements with
 *///------------------------------------------------------------------------------
	void	operator=(const Type p_Val); 

//---------------------------------------------------------------------------------
/*! Equality test operator between containers (direct comparison of memory bytes)
 *  @param p_Src source container to compare current container with
 *  @return boolean : true if both containers are equal elements by elements, else false
 *///------------------------------------------------------------------------------
	bool 	operator==(const CContainer2<Type>& p_Src) const;

//---------------------------------------------------------------------------------
/*! Inequality test operator between containers  (direct comparison of memory bytes)
 *  @param p_Src source container to compare current container with
 *  @return boolean : true if containers differ by at least one elements, else false
 *///------------------------------------------------------------------------------
	bool 	operator!=(const CContainer2<Type>& p_Src) const; 
	


protected:

//! Pointer to the container memory location
	Type**	m_pData;

//! Height of the container (1rst dimension)
	int		m_Height;

//! Width of the container (2nd dimension)
	int		m_Width;

//---------------------------------------------------------------------------------
/*! Dynamic memory allocation, but not initialized with any value.
 *  @param p_Height height of the container (1srt dimension)
 *  @param p_Width width of the container (2nd dimension)
 *  @return boolean : true if memory was successfully allocated, false if allocation failed or if new size is different than requested size.
 *///------------------------------------------------------------------------------
	bool	Alloc(const int p_Height, const int p_Width);
};

#include "Container2.cpp"

#endif //__CContainer2__

