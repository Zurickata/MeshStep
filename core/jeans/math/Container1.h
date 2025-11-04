// Array\Container1.h
#ifndef __CContainer1__
#define __CContainer1__

#include <stdio.h>

//#include <afxwin.h>
//#include <afxtempl.h>

//---------------------------------------------------------------------------------
/*! One dimension template container
 *  @image html Container1.bmp
 *
 *	*****************
 *	!!! ATTENTION !!!
 *	*****************
 *	L'opérateur [] utilisé jusqu'à présent pour affecter ou atteindre une valeur
 *	du container n'est pas fiable (les tests d'index hors limites ne sont pas valables)
 *	Utilisez dès à présent l'opérateur () qui permet de gérer les dépassements.
 *///------------------------------------------------------------------------------
template <class Type> class CContainer1
{
public: 

//---------------------------------------------------------------------------------
/*! Constructor : dynamic memory allocation, but not initialized with any value.
 *  @param p_Width size of the container, default value is 0
 *///------------------------------------------------------------------------------
  	CContainer1(const int p_Width = 0);

//---------------------------------------------------------------------------------
/*! Constructor from an existing memory location. The container elements are 
 *  initialized with given data (direct memory copy)
 *  @param p_pSrc pointer on an existing memory location containing data
 *  @param p_Width size of the container
 *///------------------------------------------------------------------------------
	CContainer1(const Type* p_pSrc, const int p_Width);

//---------------------------------------------------------------------------------
/*! Copy Constructor from an existing container.(direct memory copy)
 *  @param p_Src existing container
 *///------------------------------------------------------------------------------
   	CContainer1(const CContainer1<Type>& p_Src); 

//---------------------------------------------------------------------------------
/*! Constructor from an existing container, in the extend of a given size (direct memory copy)
 *  @param p_pSrc existing container
 *  @param p_Width size of the data to be initialized from the source container
 *///------------------------------------------------------------------------------
  	CContainer1(const CContainer1<Type>& p_Src, const int p_Width); 

//---------------------------------------------------------------------------------
/*! Destructor
 *///------------------------------------------------------------------------------
   	virtual ~CContainer1(); 

//---------------------------------------------------------------------------------
/*! Free container memory 
 *///------------------------------------------------------------------------------
	void	Free();

//---------------------------------------------------------------------------------
/*! Setting the size of the container (destroy previous memory and reallocate, but not
 *  initialized with any value)
 *  @param p_Width size of the container
 *  @return boolean : TRUE if memory was successfully allocated, else FALSE
 *///------------------------------------------------------------------------------
  	bool	SetSize(const int p_Width);

//---------------------------------------------------------------------------------
/*! Access to the size of the container
 *  @return number of elements
 *///------------------------------------------------------------------------------
	const	int& GetSize() const { return m_Width; }

//---------------------------------------------------------------------------------
/*! Access to the size of the container
 *  @return number of elements
 *///------------------------------------------------------------------------------
	const	int& Width() const { return m_Width; }

//---------------------------------------------------------------------------------
/*! Access to the number of elements 
 *  @return number of elements
 *///------------------------------------------------------------------------------
	int		GetNbElements() const { return m_Width; }

//---------------------------------------------------------------------------------
/*! Access to the size of memeory allocated for the container
 *  @return number of bytes allocated
 *///------------------------------------------------------------------------------
	int		Sizeof() const;

//---------------------------------------------------------------------------------
/*! Access to the address of the first element of the container
 *  @return pointer to the first contiguous memory location of the container
 *///------------------------------------------------------------------------------
  	Type*	GetBuffer() const { return m_pData; }

//---------------------------------------------------------------------------------
/*! Set all the the elements of the container to the same value
 *  @param p_Val value with which the container elements will be set 
 *///------------------------------------------------------------------------------
	void	SetValue(const Type p_Val); 

//---------------------------------------------------------------------------------
/*! Set a given number of contiguous container elements, starting from a given offset, 
 *  to the same value
 *  @param p_Val value with which the container elements will be set 
 *  @param p_OffX size of the offset, where the setting will start 
 *  @param p_DimX number elements to be set 
 *///------------------------------------------------------------------------------
	void	SetValue(const Type p_Val, const int p_OffX, const int p_DimX);

//---------------------------------------------------------------------------------
/*! Set values of the container from a CList object. The previous container
 *	object is delete. CList object uses functions with value transmitted arguments.
 *  @param p_List CList object from which the container elements will be set
 *	@return false if allocation failed
 *///------------------------------------------------------------------------------
	//bool	FromList(const CList<Type, Type>& p_List);

//---------------------------------------------------------------------------------
/*! Set values of the container from a CList object. The previous container
 *	object is delete. CList object uses functions with reference transmitted arguments.
 *  @param p_List CList object from which the container elements will be set
 *	@return false if allocation failed
 *///------------------------------------------------------------------------------
	//bool	FromListRef(const CList<Type, Type&>& p_List);

//---------------------------------------------------------------------------------
/*! Set values of a CList object from container's data.
 *	CList object uses functions with value transmitted arguments.
 *  @param p_List CList object that will be set
 *///------------------------------------------------------------------------------
	//void	ToList(CList<Type, Type>& p_List);

//---------------------------------------------------------------------------------
/*! Set values of a CList object from container's data.
 *	CList object uses functions with reference transmitted arguments.
 *  @param p_List CList object that will be set
 *///------------------------------------------------------------------------------
	//void	ToListRef(CList<Type, Type&>& p_List);

//---------------------------------------------------------------------------------
/*! Setting of the container with only a contiguous part of another container
 *  @param p_Src the source container
 *  @param p_OffSrcX size of the offset in the source container
 *  @param p_TailSrcX index of the last element to be copied from the source container
 *  @param p_OffDestX size of the offset in the destination container, default value is 0
 *///------------------------------------------------------------------------------
	void	GetSubArray(const CContainer1& p_Src, const int p_OffSrcX, const int p_TailSrcX, 
				const int p_OffDestX = 0);


//---------------------------------------------------------------------------------
/*! Search for a given value in the container (direct comparison of memory bytes)
 *  @param p_Val the value to look for
 *  @return boolean : TRUE if the value is found, else FALSE
 *///------------------------------------------------------------------------------
	bool	IsFound(const Type p_Val) const;	

//---------------------------------------------------------------------------------
/*! Byte swaping ( for machine compatibility )
 *///------------------------------------------------------------------------------
	void	ReverseBytes();
	

//---------------------------------------------------------------------------------
/*! Test the validity of the container
 *  @return boolean : TRUE if the memory is not allocated, else FALSE
 *///------------------------------------------------------------------------------
	bool	operator!() const; 

//---------------------------------------------------------------------------------
/*! Direct access to container elements, read and write
 *  @param p_Ind index of the element to be accessed
 *  @return a reference to the element at location p_Ind
 *///------------------------------------------------------------------------------
  	Type&	operator[](const int p_Ind) const; 

//---------------------------------------------------------------------------------
/*! Direct access to container elements, read and write
 *  @param p_Ind index of the element to be accessed
 *  @return a reference to the element at location p_Ind
 *///------------------------------------------------------------------------------
  	Type&	operator()(const int p_Ind) const;

//---------------------------------------------------------------------------------
/*! Affectation operator between containers (direct memory copy)
 *  @param p_Src source container to initialize current container with
 *///------------------------------------------------------------------------------
	void	operator=(const CContainer1<Type>& p_Src);

//---------------------------------------------------------------------------------
/*! Value affectation operator
 *  @param p_Val value to initialize the container elements with
 *///------------------------------------------------------------------------------
	void	operator=(const Type p_Val);

//---------------------------------------------------------------------------------
/*! Equality test operator between containers (direct comparison of memory bytes)
 *  @param p_Src source container to compare current container with
 *  @return boolean : TRUE if both containers are equal elements by elements, else FALSE
 *///------------------------------------------------------------------------------
	bool 	operator==(const CContainer1<Type>& p_Src) const;

//---------------------------------------------------------------------------------
/*! Inequality test operator between containers (direct comparison of memory bytes)
 *  @param p_Src source container to compare current container with
 *  @return boolean : TRUE if containers differ by at least one elements, else FALSE
 *///------------------------------------------------------------------------------
	bool 	operator!=(const CContainer1<Type>& p_Src) const; 

protected:

//! Pointer to the container memory location
	Type*	m_pData;

//! Size of the container
	int		m_Width;

//---------------------------------------------------------------------------------
/*! Dynamic memory allocation, but not initailized with any value.
 *  @param p_width size of the container
 *  @return boolean : TRUE if memory was successfully allocated, FALSE if allocation failed or if new size is different than requested size.
 *///------------------------------------------------------------------------------
	bool	Alloc(const int p_Width);

};

#include "Container1.cpp"

#endif //__CContainer1__



