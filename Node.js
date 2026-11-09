export class ProductsController {
  getById = asyncHandler(
    async (req: TypedRequest<unknown, unknown, { id: string }>, res: Response) => {
      const product = await productsService.findById(req.params.id);
      const response: ApiResponse<typeof product> = {
        success: true,
        data: product,
        message: 'Product retrieved'
      };
      res.json(response);
    }
  );
}
